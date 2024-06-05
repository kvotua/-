import { useFetchQuery } from "./useFetchQuery";
import { IProject } from "../types/project.types";

const useGetTree = <T>(projectId: string) => {
  const { data: project, isSuccess: isProjectSuccess } =
    useFetchQuery<IProject>({
      index: ["getProject", projectId],
      url: `projects/${projectId}`,
      isModalLoading: false,
    });

  const { data: tree, isSuccess: isTreeSuccess } = useFetchQuery<T>({
    index: "getTreeNodes",
    url: `/nodes/tree/${project?.core_node_id}`,
    isModalLoading: false,
    enabled: isProjectSuccess,
  });

  const { data: templates } = useFetchQuery<string[]>({
    index: "getAllTemplates",
    url: `templates/`,
    isModalLoading: false,
    enabled: isTreeSuccess,
  });
  return { tree, isTreeSuccess, templates };
};

export default useGetTree;
