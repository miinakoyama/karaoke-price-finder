export interface PlanDetail {
    plan_name: string
    general_price: number | null
    student_price: number | null
    member_price: number | null
}

export interface GetDetailResponse {
    store_id: number
    store_name: string
    phone_number?: string
    plans: PlanDetail[]
}
