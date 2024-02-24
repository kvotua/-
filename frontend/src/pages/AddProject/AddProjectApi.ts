import {
  BaseQueryFn,
  FetchArgs,
  FetchBaseQueryError,
  FetchBaseQueryMeta,
  MutationDefinition,
} from "@reduxjs/toolkit/query";
import { MutationTrigger } from "node_modules/@reduxjs/toolkit/dist/query/react/buildHooks";
import { IProject } from "src/app/store/slice/ProjectsSlice/projectsApi";

export const addProject = (
  mutation: MutationTrigger<
    MutationDefinition<
      {
        userId: number;
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
  body: IProject,
) => {
  try {
    mutation({
      userId: id,
      body,
    });
  } catch (error) {
    console.log(error);
  }
};
