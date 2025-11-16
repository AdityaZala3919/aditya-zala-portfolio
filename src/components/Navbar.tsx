import { NavLink } from "./NavLink";
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { Button } from "./ui/button";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <NavLink to="/" className="text-xl font-bold text-foreground hover:text-primary transition-colors">
            Portfolio
          </NavLink>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <NavLink
              to="/"
              className="text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
            >
              Home
            </NavLink>
            <NavLink
              to="/projects"
              className="text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
            >
              Projects
            </NavLink>
            <NavLink
              to="/blogs"
              className="text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
            >
              Blogs
            </NavLink>
            <Button asChild size="sm">
              <a href="#contact">Contact</a>
            </Button>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden text-foreground"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-4">
            <NavLink
              to="/"
              className="block text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
              onClick={() => setIsOpen(false)}
            >
              Home
            </NavLink>
            <NavLink
              to="/projects"
              className="block text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
              onClick={() => setIsOpen(false)}
            >
              Projects
            </NavLink>
            <NavLink
              to="/blogs"
              className="block text-foreground hover:text-primary transition-colors"
              activeClassName="text-primary font-medium"
              onClick={() => setIsOpen(false)}
            >
              Blogs
            </NavLink>
            <Button asChild size="sm" className="w-full">
              <a href="#contact" onClick={() => setIsOpen(false)}>Contact</a>
            </Button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
