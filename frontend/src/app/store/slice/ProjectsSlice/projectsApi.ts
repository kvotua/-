import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
export interface IProject {
  id?: string;
  name: string;
  owner_id?: string;
}

export interface CustomError {
  data: {
    detail: string;
    status: number;
  };
  status: string;
}
type ProjectsResponse = IProject[];
export const projectsApi = createApi({
  reducerPath: "projectsApi",
  tagTypes: ["Projects"],
  baseQuery: fetchBaseQuery({
    baseUrl: "http://localhost/api/v1/",
    headers: {
      "user-init-data": 'user={"id":0}',
    },
  }),
  endpoints: (builder) => ({
    getProjectsById: builder.query<IProject, string>({
      query: (projectId) => `projects/${projectId}`,
    }),
    getProjectsByUserId: builder.query<ProjectsResponse, number>({
      providesTags: ["Projects"],
      query: (userId) => `projects/by/user/${userId}`,
    }),
    addProject: builder.mutation<IProject, { body: Partial<IProject> }>({
      query: ({ body }) => ({
        url: `projects/`,
        method: "POST",
        body,
      }),
      invalidatesTags: ["Projects"],
    }),
    updateProject: builder.mutation<
      IProject,
      { body: Partial<IProject>; projectId: string }
    >({
      query: ({ body, projectId }) => ({
        url: `projects/${projectId}`,
        method: "PATCH",
        body,
      }),
      invalidatesTags: ["Projects"],
    }),
    deleteProject: builder.mutation<IProject, string>({
      query: (projectId) => ({
        url: `projects/${projectId}`,
        method: "DELETE",
      }),
      invalidatesTags: ["Projects"],
    }),
  }),
});

export const {
  useUpdateProjectMutation,
  useGetProjectsByIdQuery,
  useAddProjectMutation,
  useGetProjectsByUserIdQuery,
  useDeleteProjectMutation,
} = projectsApi;
