import axios from "axios";
import { CompetitionFormData, CompetitionDetail, Team, CreateTeamData } from "../types/competitions";

export const createCompetition = async (data: CompetitionFormData) => {
    const response = await axios.post('/api/competitions/create', {
        ...data,
        date_to_start: new Date(data.date_to_start).toISOString()
    });
    return response.data
} 

export const getCompetitions = async () => {
    const response = await axios.get('/api/competitions/all');
    return response.data;
  };

  export const getCompetitionDetail = async (id: number): Promise<CompetitionDetail> => {
    const response = await axios.get(`/api/competitions/detail/${id}`);
    return response.data;
  };
  
  export const getCompetitionTeams = async (id: number): Promise<Team[]> => {
    const response = await axios.get(`/api/competitions/${id}/teams`);
    return response.data;
  };
  
  export const createTeam = async (teamData: CreateTeamData): Promise<Team> => {
    const response = await axios.post('/api/competitions/create', teamData);
    return response.data;
  };