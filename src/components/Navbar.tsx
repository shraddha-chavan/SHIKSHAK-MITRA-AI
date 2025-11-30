import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { GraduationCap, LayoutDashboard, Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface NavbarProps {
  role: 'teacher' | 'admin';
  onRoleToggle: () => void;
}

export const Navbar = ({ role, onRoleToggle }: NavbarProps) => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const teacherLinks = [
    { to: '/', label: 'Home' },
    { to: '/teacher-dashboard', label: 'Dashboard' },
    { to: '/teacher-analytics', label: 'Analytics' },
    { to: '/activity-generator', label: 'Activities' },
  ];

  const adminLinks = [
    { to: '/', label: 'Home' },
    { to: '/management-dashboard', label: 'Dashboard' },
    { to: '/teacher-comparison', label: 'Teacher Comparison' },
    { to: '/industry-alignment', label: 'Industry Alignment' },
    { to: '/live-monitoring', label: 'Live Monitoring' },
    { to: '/reports', label: 'Reports' },
  ];

  const links = role === 'teacher' ? teacherLinks : adminLinks;

  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 font-heading text-xl font-bold">
            <GraduationCap className="h-8 w-8 text-primary" />
            <span className="bg-gradient-to-r from-primary to-info bg-clip-text text-transparent">
              Shikshak Mitra AI
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            {links.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={cn(
                  "text-sm font-medium transition-colors hover:text-primary",
                  location.pathname === link.to
                    ? "text-primary"
                    : "text-muted-foreground"
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Role Toggle */}
          <div className="flex items-center gap-4">
            <Button
              onClick={onRoleToggle}
              variant="outline"
              size="sm"
              className="gap-2"
            >
              <LayoutDashboard className="h-4 w-4" />
              <span className="hidden sm:inline">
                {role === 'teacher' ? 'Switch to Admin' : 'Switch to Teacher'}
              </span>
              <span className="sm:hidden">
                {role === 'teacher' ? 'Admin' : 'Teacher'}
              </span>
            </Button>

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X /> : <Menu />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 pt-2 space-y-2 border-t">
            {links.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                onClick={() => setMobileMenuOpen(false)}
                className={cn(
                  "block px-4 py-2 text-sm font-medium rounded-md transition-colors",
                  location.pathname === link.to
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-muted"
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
};
