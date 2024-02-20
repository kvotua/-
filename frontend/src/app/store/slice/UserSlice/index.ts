import { createSlice } from "@reduxjs/toolkit";
import { getUser } from "./userApi";

interface IUser {
  id: string;
  login: string;
}
interface IInitialState {
  user: IUser | null;
  status: string;
}

const initialState: IInitialState = {
  user: null,
  status: "",
};

export const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser(state, action) {
      state.user = action.payload;
    },
  },
  extraReducers(builder) {
    builder.addCase(getUser.fulfilled, (state, { payload }) => {
      state.user = payload;
    });
  },
});
export const { setUser } = userSlice.actions;
export default userSlice.reducer;
