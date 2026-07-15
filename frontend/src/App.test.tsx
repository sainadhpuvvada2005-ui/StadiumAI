import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { Landing } from "./pages/Landing";

test("renders STADIUMAI landing", () => {
  render(<MemoryRouter><Landing /></MemoryRouter>);
  expect(screen.getByText("STADIUMAI")).toBeInTheDocument();
});
