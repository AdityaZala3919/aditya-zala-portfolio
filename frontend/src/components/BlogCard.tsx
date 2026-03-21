import { Card, CardContent, CardHeader } from "./ui/card";
import { Badge } from "./ui/badge";
import { Calendar, Clock } from "lucide-react";

export interface Blog {
  id: number;
  title: string;
  excerpt: string;
  date: string;
  readTime: string;
  tags: string[];
  isPinned?: boolean;
}

interface BlogCardProps {
  blog: Blog;
}

const BlogCard = ({ blog }: BlogCardProps) => {
  return (
    <Card className="group hover:shadow-lg transition-all duration-300 border-border hover:border-primary cursor-pointer">
      <CardHeader>
        <div className="flex items-start justify-between gap-4 mb-2">
          <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors line-clamp-2">
            {blog.title}
          </h3>
          {blog.isPinned && (
            <Badge className="bg-accent shrink-0">Pinned</Badge>
          )}
        </div>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span className="flex items-center gap-1">
            <Calendar className="h-4 w-4" />
            {blog.date}
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            {blog.readTime}
          </span>
        </div>
      </CardHeader>
      
      <CardContent>
        <p className="text-muted-foreground mb-4 line-clamp-3">{blog.excerpt}</p>
        <div className="flex flex-wrap gap-2">
          {blog.tags.map((tag, index) => (
            <Badge key={index} variant="secondary">
              {tag}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default BlogCard;
