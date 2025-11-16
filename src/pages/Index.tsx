import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import About from "@/components/About";
import ProjectCard from "@/components/ProjectCard";
import BlogCard from "@/components/BlogCard";
import Contact from "@/components/Contact";
import Footer from "@/components/Footer";
import { projects, blogs } from "@/data/mockData";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

const Index = () => {
  const pinnedProjects = projects.filter((p) => p.isPinned).slice(0, 4);
  const pinnedBlogs = blogs.filter((b) => b.isPinned).slice(0, 3);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <Hero />
      <About />

      {/* Pinned Projects */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto">
          <div className="max-w-6xl mx-auto">
            <div className="flex items-center justify-between mb-12">
              <div>
                <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-2">
                  Featured Projects
                </h2>
                <p className="text-muted-foreground">
                  Check out some of my recent work
                </p>
              </div>
              <Button variant="outline" asChild>
                <Link to="/projects">
                  View All
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {pinnedProjects.map((project) => (
                <ProjectCard key={project.id} project={project} />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Pinned Blogs */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="container mx-auto">
          <div className="max-w-6xl mx-auto">
            <div className="flex items-center justify-between mb-12">
              <div>
                <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-2">
                  Latest Blog Posts
                </h2>
                <p className="text-muted-foreground">
                  Thoughts, tutorials, and insights
                </p>
              </div>
              <Button variant="outline" asChild>
                <Link to="/blogs">
                  View All
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {pinnedBlogs.map((blog) => (
                <BlogCard key={blog.id} blog={blog} />
              ))}
            </div>
          </div>
        </div>
      </section>

      <Contact />
      <Footer />
    </div>
  );
};

export default Index;
