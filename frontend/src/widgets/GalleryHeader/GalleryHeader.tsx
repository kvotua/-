import React from "react";
import { Outlet } from "react-router-dom";
import { InternalMenu } from "../InternalMenu/InternalMenu";
import { RoutesList } from "src/app/types/routes/types";

const GalleryHeader: React.FC = () => {
  const MenuInfo = [
    {
      path: RoutesList.Gallery,
      title: "Популярные",
    },
    {
      path: "/gallery/following/",
      title: "Избранные",
    },
    {
      path: "/gallery/new/",
      title: "Новые",
    },
    {
      path: "/gallery/personal/",
      title: "Мои",
    },
  ];
  return (
    <>
      <div className="container pt-[4vh] min-h-[100dvh]">
        <InternalMenu MenuInfo={MenuInfo} />
        <Outlet />
      </div>
    </>
  );
};

export { GalleryHeader };
