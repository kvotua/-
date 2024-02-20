import React from "react";

import { SliderProjects } from "src/widgets/SliderProjects/SliderProjects";
import { useAppSelector } from "src/app/hooks/useAppSelector";
const Home: React.FC = () => {
  const { projects } = useAppSelector((state) => state.projects);

  return (
    <div className="pt-[4vh] min-h-[100dvh]">
      <div className=" max-w-[430px] mx-auto">
        <h1 className="title">Мои проекты</h1>
        <SliderProjects projects={projects} />
      </div>
    </div>
  );
};

export { Home };
