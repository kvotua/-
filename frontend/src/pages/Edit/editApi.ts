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

export const updateProject = (
  mutation: MutationTrigger<
    MutationDefinition<
      { body: Partial<IProject>; projectId: string },
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
  navigate: NavigateFunction,
  body: IProject,
  projectId: string,
) => {
  try {
    mutation({ body, projectId })
      .then((data) =>
        "error" in data ? console.log(data.error) : navigate(-1),
      )
      .catch((err) => {
        console.log(err);
      });
  } catch (error) {
    console.log(error);
  }
};
