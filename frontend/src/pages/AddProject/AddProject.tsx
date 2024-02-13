import React, { useState } from "react";
import { InputDefault } from "src/shared/InputDefault/InputDefault";
import Back from "src/assets/back.svg?react";
import Save from "src/assets/save.svg?react";
import { useNavigate } from "react-router-dom";
import { useAddProjectMutation } from "src/app/store/slice/ProjectsSlice/projectsApi";
import { addProject } from "./AddProjectApi";
import { Menu } from "src/widgets/Menu/Menu";
const AddProject: React.FC = () => {
  const [projectName, setProjectName] = useState<string>("");
  const navigate = useNavigate();
  const [mutation] = useAddProjectMutation();

  const menuItem = [
    {
      handleClick: () => navigate(-1),
      Image: Back,
    },
    {
      handleClick: () => addProject(mutation, 0, { id: 0, name: projectName }),
      Image: Save,
    },
  ];
  return (
    <div>
      <div
        style={{ background: "linear-gradient(#7942D1, #E74EEA)" }}
        className="container pt-[4vh] min-h-[100dvh] min-w-[100vw] m-auto z-10 fixed top-0"
      >
        <div className="w-full max-w-[430px] mx-auto h-[70dvh] rounded-20 flex flex-col items-center relative z-20 gap-[20px]">
          <h2 className="text-[practice20px] font-bold uppercase text-main">
            Создать новый сайт
          </h2>
          <InputDefault
            type="text"
            name="projectName"
            handleChange={setProjectName}
            valueInp={projectName}
            placeholder="Мой проект"
          />
        </div>
        <Menu menuItem={menuItem} />
      </div>
    </div>
  );
};

export { AddProject };
