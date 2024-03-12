import { useLocation } from "react-router-dom";
import { useGetProjectsByIdQuery } from "../store/slice/ProjectsSlice/projectsApi";
import { useGetTreeNodesQuery } from "../store/slice/UserPgaeSlice/UserPageApi";

const useGetTree = () => {
  const location = useLocation();

  const regex = /\/project\/(\w{8}-(\w{4}-){3}\w{12})/;

  const projectId = location.pathname.match(regex)![1];

  const { data: project, isSuccess: isProjectSuccess } =
    useGetProjectsByIdQuery(projectId);

  const { data: tree, isSuccess: isTreeSuccess } = useGetTreeNodesQuery(
    project?.core_node_id,
    {
      skip: !isProjectSuccess,
    },
  );

  return { tree: tree, isTreeSuccess: isTreeSuccess };
};

export default useGetTree;
