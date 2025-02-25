import { z } from 'zod';

const signUpSchema = z.object({
    username: z
        .string()
        .min(3, { message: 'Username must be at least 3 characters' }),
    email: z
        .string()
        .email({ message: 'Invalid email address' }),
    password: z
        .string()
        .min(6, { message: 'Password must be at least 6 characters' }),
    confirm_password: z
        .string()
        .min(6, { message: 'Password must be at least 6 characters' }),
}).refine(data => data.password === data.confirm_password, {
    message: "Passwords must match",
    path: ["confirm_password"]
});

export type SignUpFormData = z.infer<typeof signUpSchema>