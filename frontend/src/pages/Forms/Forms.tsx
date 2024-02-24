import React, { useState } from "react";
import { InputDefault } from "src/shared/InputDefault/InputDefault";
import { UiMenu } from "src/widgets/Menu/UiMenu";
import Back from "src/assets/back.svg?react";
import Save from "src/assets/save.svg?react";
import { useNavigate } from "react-router-dom";
import { useUpdateProjectMutation } from "src/app/store/slice/ProjectsSlice/projectsApi";
import { updateProject } from "./FormsApi";
const Forms: React.FC = () => {
  const navigate = useNavigate();
  const [projectName, setProjectName] = useState<string>("");
  const [mutation] = useUpdateProjectMutation();

  const menuItem = [
    {
      handleClick: () => navigate(-1),
      Image: Back,
    },
    {
      handleClick: () =>
        updateProject(mutation, 0, { id: 0, name: projectName }),
      Image: Save,
    },
  ];

  return (
    <div className="container pt-[4vh] min-h-[100dvh] transition-[height]">
      <div className="w-full h-[70dvh] rounded-20 flex flex-col items-center relative z-20 gap-[20px]">
        <span className="text-[practice20px] font-bold uppercase text-main">
          Редактировать сайт
        </span>
        <InputDefault
          type="text"
          name="projectName"
          handleChange={setProjectName}
          valueInp={projectName}
          placeholder="Мой проект"
        />
        <span className="text-[practice20px] font-bold uppercase text-red-600">
          Удалить сайт
        </span>
      </div>
      <UiMenu menuItem={menuItem} />
    </div>
  );
};

export { Forms };
