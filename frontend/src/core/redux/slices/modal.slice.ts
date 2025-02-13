import { createSlice } from "@reduxjs/toolkit";

export const MODAL_SLICE_KEY = 'modal';

export interface ModalSliceI {
    isOpen: boolean;
    modalType: string;
    modalProps: {[key: string]: any};
}

const initialState =  {
    isOpen: false,
    modalType: '',
    modalProps: {}
} as ModalSliceI

export const modalSlice = createSlice({
    name: MODAL_SLICE_KEY,
    initialState: initialState,
    reducers: {
        openModal: (state, action) => {
            state.isOpen = true;
            state.modalType = action.payload.modalType;
            state.modalProps = action.payload.modalProps;
        },
        closeModal: (state) => {
            state = initialState
        }
    }
});