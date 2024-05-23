import React, { useState } from 'react';
import { useMutation } from "@tanstack/react-query";
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"

interface UserData {
    username: string;
    password: string;
    email?: string;
}

const SignInSignUp = () => {
    const [signInData, setSignInData] = useState<UserData>({ username: '', password: '' });
    const [signUpData, setSignUpData] = useState<UserData>({ username: '', password: '', email: '' });
    const [error, setError] = useState<string>('');

    const signInMutation = useMutation({
        mutationFn: async (formData: UserData) => {
            const response = await fetch('http://127.0.0.1:8000/api/v1/tokens/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            if (!response.ok) {
                throw new Error('Error signing in');
            }
            const responseData = await response.json();
            return responseData;
        },
        onSuccess: (data) => {
            const { token } = data;
            console.log("Token received and stored:", token);
            localStorage.setItem('token', token);
            window.location.href = '/home';
        },
        onError: () => {
            setError('Invalid username or password');
        },
    });

    const signUpMutation = useMutation({
        mutationFn: async (formData: UserData) => {
            const response = await fetch('http://127.0.0.1:8000/api/v1/users/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            if (!response.ok) {
                throw new Error('Error signing up');
            }
            const responseData = await response.json();
            return responseData;
        },
        onSuccess: (data) => {
            const { token } = data;
            console.log("Token received and stored:", token);
            localStorage.setItem('token', token);
            window.location.href = '/home';
        },
        onError: () => {
            setError('Error signing up');
        },
    });

    const handleSignInChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSignInData({ ...signInData, [e.target.name]: e.target.value });
    };

    const handleSignUpChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSignUpData({ ...signUpData, [e.target.name]: e.target.value });
    };

    const handleSignInSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError('');
        signInMutation.mutate(signInData);
    };

    const handleSignUpSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError('');
        signUpMutation.mutate(signUpData);
    };

    return (
        <div className="pt-5 bg-gray-600 my-auto h-[100vh]">
            <h1 className="text-center text-2xl font-bold mb-4 text-gray-200">Sign In / Sign Up</h1>
            {error && <p style={{ color: 'white', textAlign: 'center' }}>{error}</p>}
            <Tabs defaultValue="signin" className="w-full max-w-md mx-auto">
                <TabsList className="grid grid-cols-2">
                    <TabsTrigger value="signin">Logga In</TabsTrigger>
                    <TabsTrigger value="signup">Registrera</TabsTrigger>
                </TabsList>
                <TabsContent value="signin">
                    <Card>
                        <CardHeader>
                            <CardTitle>Logga In</CardTitle>
                            <CardDescription>
                                Om du har ett konto kan du logga in här
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleSignInSubmit}>
                                <div className="space-y-2">
                                    <Label htmlFor="signin-username">Användarnamn</Label>
                                    <Input
                                        id="signin-username"
                                        type="text"
                                        name="username"
                                        value={signInData.username}
                                        onChange={handleSignInChange}
                                        required
                                    />
                                </div>
                                <div className="space-y-2 mt-4">
                                    <Label htmlFor="signin-password">Lösenord</Label>
                                    <Input
                                        id="signin-password"
                                        type="password"
                                        name="password"
                                        value={signInData.password}
                                        onChange={handleSignInChange}
                                        required
                                    />
                                </div>
                                <Button type="submit" className='mt-3'>Logga In</Button>
                            </form>
                        </CardContent>
                    </Card>
                </TabsContent>
                <TabsContent value="signup">
                    <Card>
                        <CardHeader>
                            <CardTitle>Registrera</CardTitle>
                            <CardDescription>
                                Om du inte har ett konto kan du registrera dig
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleSignUpSubmit}>
                                <div className="space-y-2">
                                    <Label htmlFor="signup-username">Användarnamn</Label>
                                    <Input
                                        id="signup-username"
                                        type="text"
                                        name="username"
                                        value={signUpData.username}
                                        onChange={handleSignUpChange}
                                        required
                                    />
                                </div>
                                <div className="space-y-2 mt-4">
                                    <Label htmlFor="signup-email">Email</Label>
                                    <Input
                                        id="signup-email"
                                        type="email"
                                        name="email"
                                        value={signUpData.email}
                                        onChange={handleSignUpChange}
                                        required
                                    />
                                </div>
                                <div className="space-y-2 mt-4">
                                    <Label htmlFor="signup-password">Lösenord</Label>
                                    <Input
                                        id="signup-password"
                                        type="password"
                                        name="password"
                                        value={signUpData.password}
                                        onChange={handleSignUpChange}
                                        required
                                    />
                                </div>
                                <Button type="submit" className='mt-3'>Registrera</Button>
                            </form>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default SignInSignUp;
