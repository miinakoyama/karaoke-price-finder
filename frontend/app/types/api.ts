export interface PlanDetail {
    plan_name: string
    general_price: number | null
    student_price: number | null
    member_price: number | null
    time_range?: string
}

export interface GetDetailResponse {
    store_id: number
    store_name: string
    phone_number?: string
    plans: PlanDetail[]
}

export interface PlanCalc {
    plan_name: string
    time_range: string
    total_price: number
}

export interface SearchResultItem {
    store_id: number
    chain_name: string
    store_name: string
    lowest_price_per_person: number
    drink_option: string
    distance: number
    latitude: number
    longitude: number
    phone_number?: string
    plan_calc: PlanCalc[]
}
