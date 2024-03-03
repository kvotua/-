import { configureStore } from "@reduxjs/toolkit";
import user from "./slice/UserSlice";
import projects from "./slice/ProjectsSlice";
import userPage from "./slice/UserPgaeSlice";
import { projectsApi } from "./slice/ProjectsSlice/projectsApi";

export const store = configureStore({
  reducer: {
    user,
    projects,
    userPage,
    [projectsApi.reducerPath]: projectsApi.reducer,
    // [userApi.reducerPath]: userApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(projectsApi.middleware),
  // .concat(userApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
