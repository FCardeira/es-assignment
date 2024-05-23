import type { AxiosResponse } from 'axios';
import axios from '../boot/axios';
import { addAlert } from '../components/alerts/store';

export type Appointment = {
    appointment_id: number
    doctor: string
    date: string
    time: string
    speciality: string
    state: string | null
    patient_username: string
}

export type CreateAppointment = {
    doctor: string
    date: string
    time: string
    speciality: string
}

export type Slot = {
    time: string,
    doctor: string,
    date: string
}

export async function getUserAppointments(): Promise<Appointment[]> {
    try {
        const response =  await axios.get<Appointment[]>('/appointments/user');

        return response.data;
    } catch (error) {
        addAlert({ message: 'Error fetching appointments', color: 'red' });
    }
    return []
}

export async function getAppointment(appointmentId: number): Promise<Appointment | undefined> {
    try {
        const response =  await axios.get<Appointment>(`/appointments/${appointmentId}`);
        return response.data;
    } catch (error) {
        addAlert({ message: 'Error fetching appointment', color: 'red' });
    }
}

export async function getAppointmentState(appointment: Appointment): Promise<string> {
    try {
        const response =  await axios.get<string>(`/appointments/${appointment.appointment_id}/state`);
        return response.data;
    } catch (error) {
        addAlert({ message: 'Error fetching appointment state', color: 'red' });
    }
    return '-'
}

export async function payAppointment(appointmentId: number): Promise<void> {
    try {
        await axios.put(`/appointments/${appointmentId}/pay`);
    } catch (error) {
        addAlert({ message: 'Error paying appointment', color: 'red' });
    }
}

export async function getOccupiedTimeSlots(date: string, doctor: string): Promise<Slot[]> {
    try {
        const response =  await axios.get<Slot[]>('/appointments/slots', {
            params: {
                date,
                doctor
            }
        });
        return response.data;
    } catch (error) {
        addAlert({ message: 'Error fetching occupied time slots', color: 'red' });
    }
    return []
}

export async function scheduleAppointment(createAppointment: CreateAppointment): Promise<Appointment | undefined> {
    try {
        createAppointment.date = createAppointment.date.split('-').reverse().join('/');
        const reponse = await axios.post<CreateAppointment, AxiosResponse<Appointment>>('/appointments', createAppointment);
        return reponse.data;
    } catch (error) {
        addAlert({ message: 'Error scheduling appointment', color: 'red' });
    }
}