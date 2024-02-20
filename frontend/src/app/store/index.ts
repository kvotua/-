import { configureStore } from "@reduxjs/toolkit";
import user from "./slice/UserSlice";
import projects from "./slice/ProjectsSlice";
import { projectsApi } from "./slice/ProjectsSlice/projectsApi";
// import { userApi } from './slice/UserSlice/userApi'

export const store = configureStore({
  reducer: {
    user,
    projects,
    [projectsApi.reducerPath]: projectsApi.reducer,
    // [userApi.reducerPath]: userApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(projectsApi.middleware)
      // .concat(userApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
