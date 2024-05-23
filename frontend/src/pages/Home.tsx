import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

interface FormData {
    name: string;
    age: string;
    traits: string;
    programming_language: string;
    employer_link: string;
}

const capitalizeWords = (str: string) => {
    return str.replace(/\b\w/g, (char) => char.toUpperCase());
};

const fetchLetters = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error('User is not authenticated');
    }

    console.log("Token retrieved from localStorage:", token);

    const response = await fetch('http://127.0.0.1:8000/api/v1/application-creator/', {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`, 
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        if (response.status === 401) {
            throw new Error('Unauthorized: You do not have permission to access this resource');
        }
        throw new Error('Error fetching your personal letter');
    }
    const responseData = await response.json();
    return responseData.length > 0 ? responseData[responseData.length - 1] : null;
};

const Home: React.FC = () => {
    const [formData, setFormData] = useState<FormData>({
        name: '',
        age: '',
        traits: '',
        programming_language: '',
        employer_link: ''
    });
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [id]: value
        }));
    };

    const queryClient = useQueryClient();

    const { data, error, isLoading, isError } = useQuery({
        queryKey: ['output', 'skill_match'],
        queryFn: fetchLetters,
    });

    const mutation = useMutation({
        mutationFn: async (formData: FormData) => {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('User is not authenticated');
            }

            console.log("Token retrieved from localStorage:", token);

            const response = await fetch('http://127.0.0.1:8000/api/v1/application-creator/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`, 
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            if (!response.ok) {
                throw new Error('Error creating your personal letter');
            }
            const responseData = await response.json();
            return responseData;
        },
        onSuccess: () => {
            // @ts-ignore
            queryClient.invalidateQueries(['output']);
        },
        onSettled: () => {
            setIsSubmitting(false);
        }
    });

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        setIsSubmitting(true);
        mutation.mutate(formData);
    };

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (isError) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <main className="flex flex-col items-center min-h-screen bg-gray-600 text-white">
            <div className="w-[95vw]">
                <section className="container mx-auto py-10 px-6 flex flex-wrap justify-center gap-10">
                    <div className="flex flex-col w-full md:w-1/2 lg:w-2/5 gap-10">
                        <Card className="bg-gray-800 rounded-lg overflow-hidden shadow-xl transition-shadow duration-300 hover:shadow-2xl h-[37rem]">
                            <CardHeader className="p-6 bg-gray-700 border-b border-gray-600">
                                <CardTitle className="text-2xl font-bold text-white">Skapa Personligt Brev</CardTitle>
                                <CardDescription className="text-gray-400">Skapa ett helt personligt brev med ett klick.</CardDescription>
                            </CardHeader>
                            <CardContent className="p-6">
                                <form onSubmit={handleSubmit}>
                                    <Label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-1">Namn:</Label>
                                    <Input id="name" value={formData.name} onChange={handleInputChange} placeholder="Markus Oskarsson" className="mb-4 p-2 border border-gray-600 rounded-md w-full bg-gray-700 text-white" />

                                    <Label htmlFor="age" className="block text-sm font-medium text-gray-300 mb-1">Ålder:</Label>
                                    <Input id="age" value={formData.age} onChange={handleInputChange} placeholder="21" className="mb-4 p-2 border border-gray-600 rounded-md w-full bg-gray-700 text-white" />

                                    <Label htmlFor="traits" className="block text-sm font-medium text-gray-300 mb-1">Egenskaper:</Label>
                                    <Input id="traits" value={formData.traits} onChange={handleInputChange} placeholder="Positiv, Tar Initiativ, Hjälpsam etc" className="mb-4 p-2 border border-gray-600 rounded-md w-full bg-gray-700 text-white" />

                                    <Label htmlFor="programming_language" className="block text-sm font-medium text-gray-300 mb-1">Programmerings språk:</Label>
                                    <Input id="programming_language" value={formData.programming_language} onChange={handleInputChange} placeholder="JavaScript, Python" className="mb-4 p-2 border border-gray-600 rounded-md w-full bg-gray-700 text-white" />

                                    <Label htmlFor="employer_link" className="block text-sm font-medium text-gray-300 mb-1">Länk till arbetsgivare:</Label>
                                    <Input id="employer_link" value={formData.employer_link} onChange={handleInputChange} placeholder="https://volvo.se/soka_jobb" className="mb-4 p-2 border border-gray-600 rounded-md w-full bg-gray-700 text-white" />
                                    
                                    <Button type="submit" className="mt-4 w-full bg-gray-200 text-black py-2 rounded-md hover:bg-gray-400" disabled={isSubmitting}>
                                        {isSubmitting ? 'Skapar...' : 'Skapa'}
                                    </Button>
                                </form>
                            </CardContent>
                        </Card>
                        <Card className="bg-gray-800 rounded-lg overflow-hidden shadow-xl transition-shadow duration-300 hover:shadow-2xl">
                            <CardHeader className="p-6 bg-gray-700 border-b border-gray-600">
                                <CardTitle className="text-2xl font-bold text-white">Utveckla dina kunskaper</CardTitle>
                                <CardDescription className="text-gray-400">Annat som är bra att kunna för dig</CardDescription>
                            </CardHeader>
                            <CardContent className="p-6">
                                {data && data.skill_match ? (
                                    <div className="my-5 p-4 bg-gray-800 border border-gray-600 rounded-md shadow-sm text-gray-200">
                                        <ul className="list-decimal list-inside">
                                            {data.skill_match.map((skill: string, index: number) => (
                                                <li key={index}>{capitalizeWords(skill)}</li>
                                            ))}
                                        </ul>
                                    </div>
                                ) : (
                                    <div className="text-gray-400">Inga data tillgängliga. Skapa en jobbansökan först.</div>
                                )}
                            </CardContent>
                        </Card>
                    </div>
                    <Card className="w-full md:w-1/2 lg:w-2/5 bg-gray-800 rounded-lg overflow-hidden shadow-xl transition-shadow duration-300 hover:shadow-2xl">
                        <CardHeader className="p-6 bg-gray-700 border-b border-gray-600">
                            <CardTitle className="text-2xl font-bold text-white">Ditt Personliga Brev</CardTitle>
                            <CardDescription className="text-gray-400">Här kommer ditt personliga brev vara.</CardDescription>
                        </CardHeader>
                        <CardContent className="p-6">
                            {isLoading ? (
                                <h1>Loading...</h1>
                            ) : data && data.output ? (
                                <div className="my-5 p-4 bg-gray-800 border border-gray-600 rounded-md shadow-sm text-gray-200">
                                    {data.output}
                                </div>
                            ) : (
                                <div className="text-gray-400">Inga data tillgängliga. Skapa en jobbansökan först.</div>
                            )}
                        </CardContent>
                    </Card>
                </section>
                <section className="container mx-auto py-10 px-6 flex justify-center items-center">
                    <iframe
                        src="http://localhost:8501"
                        className="w-[83%] h-[500px] border-none rounded-lg shadow-lg"
                        title="Job Explorer Dashboard"
                    ></iframe>
                </section>
            </div>
        </main>
    );
};

export default Home;
