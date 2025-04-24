export enum CompetitionsType {
    OPEN = 'Открытое',
    REGIONAL = 'Региональное',
    FEDERAL = 'Федеральное'
}

export enum CompetitionsDiscipline {
    PRODUCT = 'Продуктовое программирование',
    SECURITY = 'Программирование систем информационной безопасности',
    ALGORITHMIC = 'Алгоритмическое программирование',
    ROBOTICS = 'Программирование робототехники',
    UAV = 'Программирование беспилотных авиационных систем'
}

export interface CompetitionFormData {
    title: string;
    type: CompetitionsType;
    discipline: CompetitionsDiscipline;
    date_to_start: string;
    description: string;
    max_count_users: number;
    min_age_users: number;
    region_id_list: number[];
    is_published: boolean;

}

export interface Region{
    id: number;
    region_name: string
}