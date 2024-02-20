import {
  BaseQueryFn,
  FetchArgs,
  FetchBaseQueryError,
  FetchBaseQueryMeta,
  MutationDefinition,
} from "@reduxjs/toolkit/query";
import { MutationTrigger } from "node_modules/@reduxjs/toolkit/dist/query/react/buildHooks";
import { IProject } from "src/app/store/slice/ProjectsSlice/projectsApi";

export const updateProject = (
  mutation: MutationTrigger<
    MutationDefinition<
      {
        projectId: number;
        body: Partial<IProject>;
      },
      BaseQueryFn<
        string | FetchArgs,
        unknown,
        FetchBaseQueryError,
        object,
        FetchBaseQueryMeta
      >,
      "Projects",
      IProject,
      "projectsApi"
    >
  >,
  id: number,
  body: IProject
) => {
  try {
    mutation({ body, projectId: id });
  } catch (error) {
    console.log(error);
  }
};
