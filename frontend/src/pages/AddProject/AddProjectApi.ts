import {
  BaseQueryFn,
  FetchArgs,
  FetchBaseQueryError,
  FetchBaseQueryMeta,
  MutationDefinition,
} from "@reduxjs/toolkit/query";
import { MutationTrigger } from "node_modules/@reduxjs/toolkit/dist/query/react/buildHooks";
import { NavigateFunction } from "react-router-dom";
import { IProject } from "src/app/store/slice/ProjectsSlice/projectsApi";

export const addProject = (
  mutation: MutationTrigger<
    MutationDefinition<
      { body: Partial<IProject> },
      BaseQueryFn<
        string | FetchArgs,
        unknown,
        FetchBaseQueryError,
        Record<string, unknown>,
        FetchBaseQueryMeta
      >,
      "Projects",
      IProject,
      "projectsApi"
    >
  >,
  navigate: NavigateFunction,
  body: IProject,
) => {
  mutation({ body })
    .then((data) => ("error" in data ? console.log(data.error) : navigate(-1)))
    .catch((err) => {
      console.log(err);
    });
};
