'use client'

import { GoogleMap, MarkerF, useLoadScript, MarkerClustererF } from '@react-google-maps/api'
import { Store, MembershipSettings } from '@/app/types/store'
import { useMemo } from 'react'

interface ResultsMapProps {
  stores: Store[]
  membershipSettings: MembershipSettings
}

export function ResultsMap({ stores, membershipSettings }: ResultsMapProps) {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '',
  })

  const center = useMemo(() => {
    if (stores.length > 0) {
      return { lat: stores[0].latitude, lng: stores[0].longitude }
    }
    return { lat: 35.681236, lng: 139.767125 } // Tokyo Station fallback
  }, [stores])

  const getPrice = (store: Store) => {
    const isMember =
      membershipSettings[store.chainKey as keyof MembershipSettings]?.isMember
    return isMember && store.memberPrice ? store.memberPrice : store.price
  }

  if (!isLoaded) {
    return <div className="flex items-center justify-center h-full">Loading map...</div>
  }

  return (
    <GoogleMap center={center} zoom={13} mapContainerStyle={{ width: '100%', height: '100%' }}>
      <MarkerClustererF>
        {(clusterer) => (
          <>
            {stores.map((store) => (
              <MarkerF
                key={store.id}
                position={{ lat: store.latitude, lng: store.longitude }}
                clusterer={clusterer}
                label={{
                  text: `¥${getPrice(store).toLocaleString()}`,
                  className: 'marker-label',
                }}
              />
            ))}
          </>
        )}
      </MarkerClustererF>
    </GoogleMap>
  )
}
