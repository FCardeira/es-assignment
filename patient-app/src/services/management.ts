import axios from '../boot/axios';
import type { Appointment } from './appointments';

export async function getAppointments() {
    const response = await axios.get<Appointment[]>('/manager/appointments');
    return response.data;
}

export async function finishAppointment(appointmentId: number) {
    await axios.put(`/manager/appointments/${appointmentId}/finish`);
}