import { useParams } from "react-router-dom";
import { useFetchQuery } from "./useFetchQuery";
import { IProject } from "../types/project.types";

const useGetTree = <T>() => {
  const { projectId } = useParams();

  const { data: project, isSuccess: isProjectSuccess } =
    useFetchQuery<IProject>({
      index: "getProject",
      url: `projects/${projectId}`,
      isModalLoading: false,
    });

  const { data: tree, isSuccess: isTreeSuccess } = useFetchQuery<T>({
    index: "getTreeNodes",
    url: `/nodes/tree/${project?.core_node_id}`,
    isModalLoading: false,
    enabled: isProjectSuccess,
  });
  return { tree, isTreeSuccess };
};

export default useGetTree;
