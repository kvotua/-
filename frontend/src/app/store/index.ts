import { configureStore } from "@reduxjs/toolkit";
import user from "./slice/UserSlice";
import projects from "./slice/ProjectsSlice";
import userPage from "./slice/UserPgaeSlice";
import { projectsApi } from "./slice/ProjectsSlice/projectsApi";
import { nodesApi } from "./slice/UserPgaeSlice/UserPageApi";

export const store = configureStore({
  reducer: {
    user,
    projects,
    userPage,
    [nodesApi.reducerPath]: nodesApi.reducer,
    [projectsApi.reducerPath]: projectsApi.reducer,
    // [userApi.reducerPath]: userApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(nodesApi.middleware)
      .concat(projectsApi.middleware),
  // .concat(userApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
