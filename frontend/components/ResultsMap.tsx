'use client'

import { GoogleMap, MarkerF, useLoadScript, MarkerClustererF, OverlayViewF } from '@react-google-maps/api'
import { Store, MembershipSettings } from '@/app/types/store'
import { useMemo, useState, useEffect, useRef } from 'react'

interface ResultsMapProps {
  stores: Store[]
  membershipSettings: MembershipSettings
  onMarkerClick?: (store: Store) => void
  searchLatitude?: number | null
  searchLongitude?: number | null
  searchLocation?: string
}

export function ResultsMap({ stores, membershipSettings, onMarkerClick, searchLatitude, searchLongitude, searchLocation }: ResultsMapProps) {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '',
  })

  const [showSearchInfo, setShowSearchInfo] = useState(false)
  const mapRef = useRef<google.maps.Map | null>(null)

  const center = useMemo(() => {
    if (searchLatitude && searchLongitude) {
      return { lat: searchLatitude, lng: searchLongitude }
    }
    if (stores.length > 0) {
      return { lat: stores[0].latitude, lng: stores[0].longitude }
    }
    return { lat: 35.681236, lng: 139.767125 } // Tokyo Station fallback
  }, [stores, searchLatitude, searchLongitude])

  // Google Maps APIが読み込まれた後に地図の範囲を設定
  useEffect(() => {
    if (!isLoaded || !mapRef.current) return

    if (stores.length === 0 && !searchLatitude) {
      return
    }

    const bounds = new google.maps.LatLngBounds()

    // 検索位置を範囲に追加
    if (searchLatitude && searchLongitude) {
      bounds.extend({ lat: searchLatitude, lng: searchLongitude })
    }

    // 全ての店舗を範囲に追加
    stores.forEach(store => {
      bounds.extend({ lat: store.latitude, lng: store.longitude })
    })

    // 範囲を少し拡張して余裕を持たせる
    const ne = bounds.getNorthEast()
    const sw = bounds.getSouthWest()
    const latDiff = ne.lat() - sw.lat()
    const lngDiff = ne.lng() - sw.lng()

    bounds.extend({ lat: ne.lat() + latDiff * 0.1, lng: ne.lng() + lngDiff * 0.1 })
    bounds.extend({ lat: sw.lat() - latDiff * 0.1, lng: sw.lng() - lngDiff * 0.1 })

    // 検索位置が中心になるように調整
    if (searchLatitude && searchLongitude) {
      const latDiff = Math.abs(ne.lat() - sw.lat())
      const lngDiff = Math.abs(ne.lng() - sw.lng())

      // 検索位置から最も遠い店舗までの距離を計算
      let maxDistance = 0
      stores.forEach(store => {
        const distance = Math.sqrt(
          Math.pow(store.latitude - searchLatitude, 2) +
          Math.pow(store.longitude - searchLongitude, 2)
        )
        maxDistance = Math.max(maxDistance, distance)
      })

      // 検索位置を中心とした適切な範囲を設定
      // 最大距離の1.5倍の範囲を確保して余裕を持たせる
      const displayRange = Math.max(maxDistance * 1.5, Math.max(latDiff, lngDiff) * 0.3)

      const newBounds = new google.maps.LatLngBounds()
      newBounds.extend({
        lat: searchLatitude - displayRange,
        lng: searchLongitude - displayRange
      })
      newBounds.extend({
        lat: searchLatitude + displayRange,
        lng: searchLongitude + displayRange
      })

      mapRef.current.fitBounds(newBounds)
    } else {
      mapRef.current.fitBounds(bounds)
    }
  }, [isLoaded, stores, searchLatitude, searchLongitude])

  const getPrice = (store: Store) => {
    const isMember =
      membershipSettings[store.chainKey as keyof MembershipSettings]?.isMember
    return isMember && store.memberPrice ? store.memberPrice : (store.price_per_person || 0)
  }

  if (!isLoaded) {
    return <div className="flex items-center justify-center h-full">Loading map...</div>
  }

  return (
    <GoogleMap
      center={center}
      zoom={13}
      mapContainerStyle={{ width: '100%', height: '100%' }}
      options={{
        gestureHandling: 'greedy'
      }}
      onLoad={(map) => {
        mapRef.current = map
      }}
    >
      {/* 検索位置のマーカー */}
      {searchLatitude && searchLongitude && (
        <>
          <MarkerF
            position={{ lat: searchLatitude, lng: searchLongitude }}
            icon={{
              url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <!-- ピンの影 -->
                  <ellipse cx="24" cy="44" rx="4" ry="2" fill="rgba(0,0,0,0.2)"/>
                  <!-- ピンの本体 -->
                  <path d="M24 4C16.27 4 10 10.27 10 18c0 10.5 14 26 14 26s14-15.5 14-26c0-7.73-6.27-14-14-14z" fill="#F97316" stroke="white" stroke-width="2"/>
                  <!-- 検索マーク -->
                  <circle cx="20" cy="16" r="6" fill="white"/>
                  <path d="m26 22 4 4" stroke="#F97316" stroke-width="2" stroke-linecap="round"/>
                </svg>
              `),
              scaledSize: new google.maps.Size(48, 48),
              anchor: new google.maps.Point(24, 48),
            }}
            onClick={() => setShowSearchInfo(true)}
          />
          {showSearchInfo && (
            <OverlayViewF
              position={{ lat: searchLatitude, lng: searchLongitude }}
              mapPaneName="overlayMouseTarget"
              getPixelPositionOffset={(width, height) => ({
                x: -(width / 2),
                y: -height - 60 // マーカーの真下に配置（マーカーの高さ48px + 余白12px）
              })}
            >
              <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-3 max-w-xs">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <span className="text-orange-600 mr-2">🔍</span>
                    <span className="font-bold text-orange-600">検索位置</span>
                  </div>
                  <button
                    onClick={() => setShowSearchInfo(false)}
                    className="text-gray-400 hover:text-gray-600 ml-2"
                  >
                    ✕
                  </button>
                </div>
                {searchLocation && (
                  <div className="text-sm text-gray-600 mt-1">{searchLocation}</div>
                )}
              </div>
            </OverlayViewF>
          )}
        </>
      )}

      <MarkerClustererF>
        {(clusterer) => (
          <>
            {stores.map((store) => (
              <MarkerF
                key={store.shop_id}
                position={{ lat: store.latitude, lng: store.longitude }}
                clusterer={clusterer}
                label={{
                  text: `¥${getPrice(store).toLocaleString()}`,
                  color: '#fff',
                  className: 'marker-label',
                }}
                onClick={() => onMarkerClick?.(store)}
              />
            ))}
          </>
        )}
      </MarkerClustererF>
    </GoogleMap>
  )
}
