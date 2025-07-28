import axios from "axios";

const api = axios.create({
  baseURL: "/api/store/",
});

export const getEvents = () =>
  api.get("events/").then((res) => res.data.results);
export const getContents = () =>
  api.get("contents/").then((res) => res.data.results);
