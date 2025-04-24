import axios from "axios";
import { CompetitionFormData } from "../types/competitions";

export const createCompetition = async (data: CompetitionFormData) => {
    const response = await axios.post('/api/competitions/create', {
        ...data,
        date_to_start: new Date(data.date_to_start).toISOString()
    });
    return response.data
}