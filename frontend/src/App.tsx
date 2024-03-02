import { useEffect } from "react";
import { AppRoute } from "./app/routes/AppRoute";
import { tg } from "./app/tg";
import { IUser } from "./pages/Profile/Profile";
import { useAppDispatch } from "./app/hooks/useAppDispatch";
import { getUser } from "./app/store/slice/UserSlice/userApi";

// interface telegram {
//   id: number;
//   first_name: string;
//   last_name: string;
// }

function App() {
  // const dispatch = useAppDispatch();
  // let navigate = useNavigate();
  // const tgUser: telegram = tg.initDataUnsafe.user;
  const tgUser: IUser = tg.initDataUnsafe.user;
  const dispatch = useAppDispatch();

  useEffect(() => {
    // const projectId = localStorage.getItem("projectId");
    // if (!projectId) navigate("/");
    tg.ready();
    tg.expand();
    tg.enableClosingConfirmation();
    // if (tgUser && tgUser.id) {
    //   dispatch(getUser(tgUser.id));
    // }
    // // Локальные данные
    // else {
    // }
    dispatch(getUser("0"));
    // async function validUser() {
    //   if (tgUser === undefined) {
    //     dispatch(getUserWithProjectsByIdThunk({ userId: "string" }));
    //   } else {
    //     const resp = await getUserById(`${tgUser.id}`);
    //     if (resp.status === 400) {
    //       await postUserById(`${tgUser.id}`, {
    //         first_name: `${tgUser.first_name}`,
    //         last_name: `${tgUser.last_name}`,
    //         birthday: "",
    //         phone_number: "",
    //         bio: "",
    //         status: "",
    //       });
    //       const resp2 = await getUserById(`${tgUser.id}`);
    //       dispatch(setUser(await resp2.user));
    //     } else {
    //       dispatch(getUserWithProjectsByIdThunk({ userId: `${tgUser.id}` }));
    //     }
    //   }
    // }
    // validUser();
  }, [tgUser, dispatch]);
  // if (
  //   !/Android|webOS|iPhone|iPad|iPod|BlackBerry|BB|PlayBook|IEMobile|Windows Phone|Kindle|Silk|Opera Mini/i.test(
  //     navigator.userAgent
  //   )
  // ) {
  //   return <div className="min-h-screen">no</div>;
  // }
  return (
    <>
      <AppRoute />
    </>
  );
}

export default App;
