export enum CompetitionsType {
    OPEN = 'Открытое',
    REGIONAL = 'Региональное',
    FEDERAL = 'Федеральное'
}

export interface Competition extends Omit<CompetitionFormData, 'region_id_list'> {
    id: number;
    date_to_create: string;
    creator_id: number;
    region_id_list: number[];
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
export interface CompetitionDetail {
    id: number;
    title: string;
    date_to_start: string;
    date_to_create: string;
    discipline: string;
    description: string;
    max_count_users: number;
    min_age_users: number;
    creator_id: number;
    is_published: boolean;
    region?: Region[];
  }
  
  export interface TeamMember {
    user_id: number;
    login: string;
    username: string;
    status: string;
  }
  export interface Team {
    id: number;
    name: string;
    description: string;
    competitions_id: number;
    captain_id: number;
    pepresentative_id: number | null;
    status: string;
    login: string;
    username: string;
    members: TeamMember[];
  }
  
  export interface User {
    id: number;
    login: string
    username: string;
    role: 'Спортсмены' | 'Капитаны' | 'Всероссийская Федерация спортивоного программирования';
  }
  
  export interface CreateTeamData {
    name: string;
    description: string;
    competitions_id: number;
    users_id_list: number[];
    captain_id?: number;
    status: string;
  }