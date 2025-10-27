# 🎨 BFA Brand Guidelines

## Logo

<div align="center">
  <img src="./public/logo.svg" alt="BFA Logo" width="300"/>
</div>

### Logo Concept

The BFA logo represents the perfect fusion of **technology** and **human expertise**:

- **Left Brain (Orange/Red)**: Circuit board patterns symbolizing AI, technology, and digital innovation
- **Right Brain (Teal/Green)**: Organic tree/neural patterns representing human intelligence, nature, and growth
- **Unified Whole**: The combination shows that true intelligence comes from balancing artificial and human intelligence

## Color Palette

### Primary Colors

#### Technology Gradient (Left Brain)
```
Primary Orange:  #FF7A00  rgb(255, 122, 0)
Dark Orange/Red: #C41E3A  rgb(196, 30, 58)

CSS: linear-gradient(135deg, #FF7A00 0%, #C41E3A 100%)
```

#### Nature Gradient (Right Brain)
```
Primary Teal:    #2B7A78  rgb(43, 122, 120)
Dark Teal:       #17545A  rgb(23, 84, 90)

CSS: linear-gradient(135deg, #2B7A78 0%, #17545A 100%)
```

#### Brand Dark
```
Brand Dark:      #1A4645  rgb(26, 70, 69)
Use for: Primary text, headers, footer background
```

### Secondary Colors

#### Neutral Grays
```
Gray 50:  #F9FAFB  - Backgrounds
Gray 100: #F3F4F6  - Light backgrounds
Gray 200: #E5E7EB  - Borders
Gray 300: #D1D5DB  - Dividers
Gray 400: #9CA3AF  - Disabled elements
Gray 500: #6B7280  - Muted text
Gray 600: #4B5563  - Secondary text
Gray 700: #374151  - Body text
Gray 800: #1F2937  - Strong text
Gray 900: #111827  - Headings
```

#### Semantic Colors
```
Success: #10B981  - Completed, positive
Warning: #F59E0B  - In progress, caution
Error:   #EF4444  - Failed, negative
Info:    #3B82F6  - Information, neutral
```

## Typography

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
             'Helvetica Neue', Arial, sans-serif;
```

### Font Sizes
```
xs:   12px  - Labels, captions
sm:   14px  - Small text, metadata
base: 16px  - Body text
lg:   18px  - Subtitles
xl:   20px  - Section headers
2xl:  24px  - Card titles
3xl:  30px  - Page subtitles
4xl:  36px  - Page titles
5xl:  48px  - Hero titles
6xl:  60px  - Display titles
```

### Font Weights
```
Light:     300  - Decorative
Normal:    400  - Body text
Medium:    500  - Emphasis
Semibold:  600  - Buttons, important
Bold:      700  - Headers
Extrabold: 800  - Display text
```

## Spacing System

Based on 4px base unit:

```
xs:   4px   - Tight spacing
sm:   8px   - Small gaps
md:   16px  - Standard spacing (base)
lg:   24px  - Section spacing
xl:   32px  - Large gaps
2xl:  48px  - Page sections
3xl:  64px  - Major sections
4xl:  96px  - Hero sections
```

## Border Radius

```
sm:   4px    - Small elements, badges
md:   8px    - Inputs, buttons
lg:   12px   - Cards (small)
xl:   16px   - Cards (large)
2xl:  24px   - Panels, modals
full: 9999px - Pills, avatar
```

## Shadows

```css
/* Subtle */
sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);

/* Standard */
md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
    0 2px 4px -1px rgba(0, 0, 0, 0.06);

/* Elevated */
lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 
    0 4px 6px -2px rgba(0, 0, 0, 0.05);

/* High elevation */
xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 
    0 10px 10px -5px rgba(0, 0, 0, 0.04);

/* Maximum elevation */
2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);

/* Inset */
inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
```

## Component Styles

### Buttons

#### Primary Button
```css
background: linear-gradient(90deg, #FF7A00 0%, #2B7A78 100%);
color: white;
padding: 8px 24px;
border-radius: 12px;
font-weight: 600;
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);

/* Hover */
transform: translateY(-2px);
box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
```

#### Secondary Button
```css
background: transparent;
border: 2px solid #2B7A78;
color: #2B7A78;
padding: 8px 24px;
border-radius: 12px;
font-weight: 600;

/* Hover */
background: #2B7A78;
color: white;
```

### Cards
```css
background: white;
border-radius: 16px;
padding: 32px;
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
transition: all 300ms ease-in-out;

/* Hover */
transform: translateY(-4px);
box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

### Status Badges
```css
/* Completed */
background: #10B981;
color: white;
padding: 4px 8px;
border-radius: 9999px;
font-size: 12px;
font-weight: 600;
text-transform: uppercase;

/* In Progress */
background: #F59E0B;

/* Pending */
background: #9CA3AF;
```

## Animations

### Transitions
```css
/* Fast - UI feedback */
transition: all 150ms ease-in-out;

/* Base - Standard interactions */
transition: all 300ms ease-in-out;

/* Slow - Complex animations */
transition: all 500ms ease-in-out;
```

### Keyframe Animations
```css
/* Fade In */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Slide In */
@keyframes slideIn {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
```

## Responsive Breakpoints

```css
/* Mobile first approach */

/* Small phones */
@media (max-width: 640px) { }

/* Tablets */
@media (max-width: 768px) { }

/* Small laptops */
@media (max-width: 1024px) { }

/* Desktops */
@media (max-width: 1280px) { }

/* Large screens */
@media (max-width: 1536px) { }
```

## Usage Examples

### Gradient Text
```css
.gradient-text {
  background: linear-gradient(90deg, #FF7A00 0%, #2B7A78 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Glass Effect
```css
.glass-effect {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}
```

## Accessibility

### Contrast Ratios
- Text on white background: Use Gray 700 or darker (minimum 4.5:1)
- Large text (18px+): Use Gray 600 or darker (minimum 3:1)
- Interactive elements: Maintain 3:1 contrast with surroundings

### Focus States
```css
button:focus-visible,
input:focus-visible {
  outline: 2px solid #2B7A78;
  outline-offset: 2px;
}
```

## Do's and Don'ts

### ✅ Do's
- Use the brand gradients for primary CTAs and hero elements
- Maintain consistent spacing using the 4px grid system
- Use subtle shadows to create depth hierarchy
- Keep animations smooth and purposeful
- Ensure sufficient contrast for accessibility

### ❌ Don'ts
- Don't use colors outside the defined palette
- Don't mix different spacing systems
- Don't overuse animations - keep them subtle
- Don't compromise accessibility for aesthetics
- Don't stretch or distort the logo

## Brand Voice

### Personality
- **Professional** yet **approachable**
- **Innovative** yet **trustworthy**
- **Technical** yet **human-centered**

### Tone
- Clear and concise
- Confident but not arrogant
- Helpful and supportive
- Forward-thinking

---

**Remember**: The BFA brand represents the harmony between technology and human intelligence. Every design decision should reflect this balance.
