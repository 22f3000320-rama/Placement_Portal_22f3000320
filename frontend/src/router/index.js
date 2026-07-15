import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AdminLogin from "../components/admin/AdminLogin.vue";
import AdminDashboard from "../components/admin/AdminDashboard.vue";
import StudentLogin from "../components/student/StudentLogin.vue";
import StudentRegistration from "../components/student/StudentRegistration.vue"
import StudentDashboard from "../components/student/StudentDashboard.vue";
import CompanyDashboard from "../components/company/CompanyDashboard.vue";
import Companies from "../components/common/Companies.vue";
import CompanyDetails from "../components/company/CompanyDetails.vue";
import Students from "../components/admin/Students.vue";
import StudentDetails from "../components/admin/StudentDetails.vue";
import PendingDrives from "../components/drive/PendingDrives.vue";
import OngoingDrives from "../components/drive/OngoingDrives.vue";
import CreateDrive from "../components/drive/CreateDrive.vue";
import ClosedDrives from "../components/drive/ClosedDrives.vue";
import RejectedDrives from "../components/drive/RejectedDrives.vue";
import DriveDetails from "../components/drive/DriveDetails.vue";
import CompanyApplications from "../components/admin/CompanyApplications.vue";
import ApplicationDetails from "../components/common/ApplicationDetails.vue";
import StudentApplicationHistory from "../components/student/StudentApplicationHistory.vue";
import StudentDriveApplications from "../components/admin/StudentDriveApplications.vue";
import StudentProfile from "../components/student/StudentProfile.vue";
import Search from "../components/common/Search.vue";
import DriveSearch from "../components/common/DriveSearch.vue";
import CompanyLogin from "../components/company/CompanyLogin.vue";
import CompanyRegistration from "../components/company/CompanyRegistration.vue";
import AdminSearchStudents from "../components/admin/AdminSearchStudents.vue";


const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView,
    },
    {
        path: "/admin",
        name: "admin-login",
        component: AdminLogin
    },
    {
        path: "/admin/dashboard",
        component: AdminDashboard,
        children: [
            {
                path: "",
                redirect: {
                    name: "admin-companies"
                }
            },
            {
                path: "companies",
                name: "admin-companies",
                component: Companies,
                props:true
            },
            {
                path: "companies/:companyId",
                name: "admin-company-details",
                component: CompanyDetails,
                props: true
            },
            {
                path: "students",
                name: "admin-students",
                component: Students,
                props:true
            },
            {
                path: "students/:studentId",
                name: "admin-student-details",
                component: StudentDetails,
                props: true
            },
            {
                path: "students/application-history/:studentId",
                name: "admin-student-application-history",
                component: StudentApplicationHistory,
                props: true
            },
            {
                path: "company-applications",
                name: "admin-company-applications",
                component: CompanyApplications,
                props:true
            },
            {
                path: "student-applications",
                name: "admin-student-applications",
                component: StudentDriveApplications,
                props: true
            },
            {
                path: "applications/:applicationId",
                name: "admin-application-details",
                component: ApplicationDetails,
                props: true
            },
            {
                path: "pending-drives",
                name: "admin-pending-drives",
                component: PendingDrives,
                props:true
            },
            {
                path: "ongoing-drives",
                name: "admin-ongoing-drives",
                component: OngoingDrives,
                props:true
            },
            {
                path: "closed-drives",
                name: "admin-closed-drives",
                component: ClosedDrives,
                props:true
            },
            {
                path: "rejected-drives",
                name: "admin-rejected-drives",
                component: RejectedDrives,
                props:true
            },
            {
                path: "drives/:driveId",
                name: "admin-drive-details",
                component: DriveDetails,
                props: true
            },
            {
                path: "search",
                name: "admin-search",
                component: Search,
                props: true
            },
            {
                path: "search/drive",
                name: "admin-search-drives",
                component: DriveSearch,
                props: true
            },
            {
                path: "search/student",
                name: "admin-search-students",
                component: AdminSearchStudents,
                props: true
            },
        ]
    },
    {
        path: "/student",
        name: "student-login",
        component: StudentLogin
    },
    {
        path: "/student/register",
        name: "student-register",
        component: StudentRegistration
    },
    {
        path: "/student/dashboard",
        component: StudentDashboard,
        children: [
            {
                path: "",
                redirect: {
                    name: "student-companies"
                }
            },
            {
                path: "companies",
                name: "student-companies",
                component: Companies,
                props: true
            },
            {
                path: "companies/:companyId",
                name: "student-company-details",
                component: CompanyDetails,
                props: true
            },
            {
                path: "drives/:driveId",
                name: "student-drive-details",
                component: DriveDetails,
                props: true
            },
            {
                path: "student-applications",
                name: "student-applications",
                component: StudentDriveApplications,
                props: true
            },
            {
                path: "applications/:applicationId",
                name: "student-application-details",
                component: ApplicationDetails,
                props: true
            },
            {
                path: "profile/:studentId",
                name: "student-profile",
                component: StudentProfile,
                props:true
            },
            {
                path: "history/:studentId",
                name: "student-application-history",
                component: StudentApplicationHistory,
                props:true
            },
            {
                path: "search",
                name: "student-search",
                component: Search,
                props: true
            },
            {
                path: "search/drive",
                name: "student-search-drives",
                component: DriveSearch,
                props: true
            },
        ],
    },
    {
        path: "/company",
        name: "company-login",
        component: CompanyLogin
    },
    {
        path: "/company/register",
        name: "company-register",
        component: CompanyRegistration
    },
    {
        path: "/company/dashboard",
        component: CompanyDashboard,
        children: [
            {
                path: "",
                redirect: {
                    name: "company-ongoing-drives"
                }
            },
            {
                path: "drive-applications/:driveId",
                name: "company-drive-applications",
                component: StudentDriveApplications,
                props: true
            },
            {
                path: "drives/create",
                name: "company-create-drive",
                component: CreateDrive,
                props: true
            },
            {
                path: "drives/:driveId",
                name: "company-drive-details",
                component: DriveDetails,
                props: true
            },
            {
                path: "pending-drives",
                name: "company-pending-drives",
                component: PendingDrives,
                props: true
            },
            {
                path: "ongoing-drives",
                name: "company-ongoing-drives",
                component: OngoingDrives,
                props: true
            },
            {
                path: "rejected-drives",
                name: "company-rejected-drives",
                component: RejectedDrives,
                props: true
            },
            {
                path: "closed-drives",
                name: "company-closed-drives",
                component: ClosedDrives,
                props: true
            },
            {
                path: "applications/:applicationId",
                name: "company-application-details",
                component: ApplicationDetails,
                props: true
            }
        ]
    },
    {
        path: "/:pathMatch(.*)*",
        redirect: "/",
    },
];


const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from) => {
    const token = localStorage.getItem("access_token");

    if (to.path === "/admin" && token) {
        return { name: "admin-companies" };
    }
    if (to.path.startsWith("/admin/dashboard") && !token) {
        return { name: "admin-login" };
    }

    if (to.path === "/student" && token) {
        return { name: "student-companies" };
    }
    if (to.path === "/student/register" && token) {
        return { name: "student-companies" };
    }
    if (to.path.startsWith("/student/dashboard") && !token) {
        return { name: "student-login" };
    }

    if (to.path === "/company" && token) {
        return { name: "company-ongoing-drives" };
    }
    if (to.path === "/company/register" && token) {
        return { name: "company-ongoing-drives" };
    }
    if (to.path.startsWith("/company/dashboard") && !token) {
        return { name: "company-login" };
    }
});

export default router;