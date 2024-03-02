import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  useDeleteProjectMutation,
  useUpdateProjectMutation,
} from "src/app/store/slice/ProjectsSlice/projectsApi";
import { updateProject } from "./editApi";
import Back from "src/assets/back.svg?react";
import Save from "src/assets/save.svg?react";
import { InputDefault } from "src/shared/InputDefault/InputDefault";
import { Menu } from "src/widgets/Menu/Menu";

const Edit: React.FC = () => {
  const navigate = useNavigate();
  const [projectName, setProjectName] = useState<string>("");
  const { projectId } = useParams();
  const [updateProjectMutation] = useUpdateProjectMutation();
  const [deleteProjectMutation] = useDeleteProjectMutation();

  const menuItem = [
    {
      handleClick: () => navigate(-1),
      Image: Back,
    },
    {
      handleClick: () =>
        updateProject(
          updateProjectMutation,
          navigate,
          { name: projectName },
          projectId!,
        ),
      Image: Save,
    },
  ];

  const deleteProject = () => {
    deleteProjectMutation(projectId!)
      .then((data) =>
        "error" in data ? console.log(data.error) : navigate(-1),
      )
      .catch((err) => {
        console.log(err);
      });
  };
  return (
    <div className="container pt-[4vh] min-h-[100dvh] transition-[height]">
      <div className="w-full h-[70dvh] rounded-20 flex flex-col items-center relative z-20 gap-[20px]">
        <span className="text-[practice20px] font-bold uppercase text-main">
          Редактировать сайт.
        </span>
        <InputDefault
          type="text"
          name="projectName"
          handleChange={setProjectName}
          valueInp={projectName}
          placeholder="Мой проект"
        />
        <span
          onClick={deleteProject}
          className="text-[practice20px] font-bold uppercase text-red-600"
        >
          Удалить сайт
        </span>
      </div>
      <Menu menuItem={menuItem} />
    </div>
  );
};

export { Edit };
