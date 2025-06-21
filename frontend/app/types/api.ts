export interface PlanDetail {
    plan_name: string
    unit: string
    price: number
    price_per_30_min?: number
    start: string
    end: string
    customer_type: string[]
}

export interface GetDetailResponse {
    shop_id: string
    name: string
    plans: PlanDetail[]
}