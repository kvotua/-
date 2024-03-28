import React from "react";
import Edit from "src/app/assets/icons/edit.svg?react";
import LinkIcon from "src/app/assets/icons/link.svg?react";
import { Link, useNavigate } from "react-router-dom";
import { type IProjectCard } from "./projectCardModel";

const ProjectCard: React.FC<IProjectCard> = ({ title, id }) => {
  const navigate = useNavigate();
  return (
    <Link
      to={`/project/${id}`}
      className="bg-main rounded-20 text-center p-[20px] flex flex-col justify-between min-h-[60dvh]"
    >
      <h2 className="text-[practice20px] font-bold">{title}</h2>
      <div className="flex justify-between">
        <div
          onClick={(e) => {
            e.preventDefault();
            navigate(`/project/${id}/edit`);
          }}
        >
          <Edit stroke="black" />
        </div>
        <LinkIcon fill="black" />
      </div>
    </Link>
  );
};

export { ProjectCard };
