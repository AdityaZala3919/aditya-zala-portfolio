import { Card, CardContent, CardFooter, CardHeader } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { ExternalLink, Github } from "lucide-react";

export interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  technologies: string[];
  githubUrl?: string;
  liveUrl?: string;
  isPinned?: boolean;
}

interface ProjectCardProps {
  project: Project;
}

const ProjectCard = ({ project }: ProjectCardProps) => {
  return (
    <Card className="overflow-hidden group hover:shadow-lg transition-all duration-300 border-border hover:border-primary">
      <div className="relative overflow-hidden aspect-video bg-muted">
        <img
          src={project.image}
          alt={project.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        {project.isPinned && (
          <Badge className="absolute top-4 right-4 bg-accent">Pinned</Badge>
        )}
      </div>
      
      <CardHeader>
        <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">
          {project.title}
        </h3>
      </CardHeader>
      
      <CardContent>
        <p className="text-muted-foreground mb-4">{project.description}</p>
        <div className="flex flex-wrap gap-2">
          {project.technologies.map((tech, index) => (
            <Badge key={index} variant="secondary">
              {tech}
            </Badge>
          ))}
        </div>
      </CardContent>
      
      <CardFooter className="gap-2">
        {project.githubUrl && (
          <Button variant="outline" size="sm" asChild className="flex-1">
            <a href={project.githubUrl} target="_blank" rel="noopener noreferrer">
              <Github className="mr-2 h-4 w-4" />
              Code
            </a>
          </Button>
        )}
        {project.liveUrl && (
          <Button size="sm" asChild className="flex-1">
            <a href={project.liveUrl} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="mr-2 h-4 w-4" />
              Live Demo
            </a>
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};

export default ProjectCard;
