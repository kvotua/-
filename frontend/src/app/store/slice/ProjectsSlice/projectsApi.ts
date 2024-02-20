import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
export interface IProject {
  id: number;
  name: string;
}
type ProjectsResponse = IProject[];
export const projectsApi = createApi({
  reducerPath: "projectsApi",
  tagTypes: ["Projects"],
  baseQuery: fetchBaseQuery({ baseUrl: "http:localhost:8000/" }),
  endpoints: (builder) => ({
    getProjectsById: builder.query<ProjectsResponse, void>({
      query: (projectId) => `projects/user/${projectId}`,
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Projects" as const, id })),
              { type: "Projects", id: "LIST" },
            ]
          : [{ type: "Projects", id: "LIST" }],
    }),
    addProject: builder.mutation<
      IProject,
      { userId: number; body: Partial<IProject> }
    >({
      query: ({ userId, body }) => ({
        url: `/projects/add/${userId}`,
        method: "POST",
        body,
      }),
      invalidatesTags: [{ type: "Projects" as const, id: "LIST" }],
    }),
    updateProject: builder.mutation<
      IProject,
      { projectId: number; body: Partial<IProject> }
    >({
      query: ({ projectId, body }) => ({
        url: `/projects/edit/${projectId}`,
        method: "PUT",
        body,
      }),
      invalidatesTags: [{ type: "Projects" as const, id: "LIST" }],
    }),
    deleteProject: builder.mutation<void, number>({
      query: (projectId) => ({
        url: `projects/delete/${projectId}`,
        method: "DELETE",
      }),
      invalidatesTags: [{ type: "Projects" as const, id: "LIST" }],
    }),
  }),
});

export const {
  useUpdateProjectMutation,
  useGetProjectsByIdQuery,
  useAddProjectMutation,
  useDeleteProjectMutation,
} = projectsApi;
