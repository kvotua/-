import Gallery from "src/assets/gallery.svg?react";
import Home from "src/assets/home.svg?react";
import Profile from "src/assets/profile.svg?react";
import Info from "src/assets/info.svg?react";
import { RoutesList } from "src/app/types/routes/types";

export const menuItem = [
  {
    link: RoutesList.Home,
    Image: Home,
  },
  {
    link: RoutesList.Gallery,
    Image: Gallery,
  },
  {
    link: RoutesList.Info,
    Image: Info,
  },
  {
    link: RoutesList.Profile,
    Image: Profile,
  },
];

export const menuItem2 = [
  {
    link: RoutesList.Home,
    Image: Home,
  },
  {
    link: RoutesList.Gallery,
    Image: Gallery,
  },
];
