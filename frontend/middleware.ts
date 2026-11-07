import { NextResponse, type NextRequest } from "next/server";

const authPages = ["/login", "/register", "/forgot-password"];
const emailLinkPages = ["/verify-email", "/reset-password"];

export function middleware(request: NextRequest) {
  const { pathname, search } = request.nextUrl;
  const token = request.cookies.get("access_token");
  const isLoggedIn = Boolean(token && token.value);

  // Email link pages are always accessible
  if (emailLinkPages.some((p) => pathname.startsWith(p))) {
    return NextResponse.next();
  }

  const isAuthPage = authPages.some((p) => pathname === p || pathname.startsWith(`${p}/`));

  if (!isLoggedIn && !isAuthPage) {
    const loginUrl = new URL("/login", request.url);
    if (pathname !== "/") {
      loginUrl.searchParams.set("next", `${pathname}${search}`);
    }
    return NextResponse.redirect(loginUrl);
  }

  if (isLoggedIn && isAuthPage) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|art/|images/|_next/static|_next/image|favicon.ico).*)"],
};
