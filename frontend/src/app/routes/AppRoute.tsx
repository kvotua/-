import React from "react";
import { Route, Routes } from "react-router-dom";
import {
  appRoutes,
  galleryRoutes,
  profileRoutes,
  projectRoutes,
} from "./routes";
import { Menu } from "src/widgets/Menu/Menu";
import { ProfileHeader } from "src/widgets/ProfileHeader/ProfileHeader";
import { GalleryHeader } from "src/widgets/GalleryHeader/GalleryHeader";
import { menuItem } from "./menuListItem";

const AppRoute: React.FC = () => {
  return (
    <>
      <Routes>
        <Route element={<Menu menuItem={menuItem} />}>
          {appRoutes.map(({ Component, path }) => (
            <Route key={path} path={path} element={<Component />} />
          ))}
          <Route element={<ProfileHeader />}>
            {profileRoutes.map(({ Component, path }) => (
              <Route key={path} path={path} element={<Component />} />
            ))}
          </Route>
          <Route element={<GalleryHeader />}>
            {galleryRoutes.map(({ Component, path }) => (
              <Route key={path} path={path} element={<Component />} />
            ))}
          </Route>
        </Route>
        {projectRoutes.map(({ Component, path }) => (
          <Route key={path} path={path} element={<Component />} />
        ))}
      </Routes>
    </>
  );
};

export { AppRoute };
