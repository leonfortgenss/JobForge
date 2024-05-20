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
    programmingLanguage: string,
    employerLink: string;
}

const Home: React.FC = () => {
    const [formData, setFormData] = useState<FormData>({
        name: '',
        age: '',
        traits: '',
        programmingLanguage: '',
        employerLink: ''
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [id]: value
        }));
        console.log("formData", formData);
    };

    const queryClient = useQueryClient();

    const { data, error, isLoading, isError } = useQuery({
        queryKey: ['output'],
        queryFn: async () => {
            const response = await fetch('http://127.0.0.1:8000/api/v1/application-creator/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (!response.ok) {
                throw new Error('Error fetching your personal letter');
            }
            const responseData = await response.json();
            console.log("Fetched data:", responseData);
            // Return the latest entry
            return responseData[responseData.length - 1];
        },
    });

    const mutation = useMutation({
        mutationFn: async (formData: FormData) => {
            const response = await fetch('http://127.0.0.1:8000/api/v1/application-creator/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            if (!response.ok) {
                throw new Error('Error creating your personal letter');
            }
            const responseData = await response.json();
            console.log("Mutation response data:", responseData);
            return responseData;
        },
        onSuccess: () => {
            // @ts-ignore
            queryClient.invalidateQueries(['output']);
        },
    });

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
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
            <div className="w-[90vw]">
                <section className="container mx-auto py-10 px-6 flex flex-wrap justify-center gap-10">
                    <Card className="w-full md:w-2/5 lg:w-1/3 bg-gray-800 rounded-lg overflow-hidden shadow-xl transition-shadow duration-300 hover:shadow-2xl">
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

                                <Label htmlFor="programmingLanguage" className="block text-sm font-medium text-gray-300 mb-1">Programmerings språk:</Label>
                                <Input id="programmingLanguage" value={formData.programmingLanguage} onChange={handleInputChange} placeholder="JavaScript, Python" className="mb-4 p-2 border border-gray-600 rounded-md w-full bg-gray-700 text-white" />

                                <Label htmlFor="employerLink" className="block text-sm font-medium text-gray-300 mb-1">Länk till arbetsgivare:</Label>
                                <Input id="employerLink" value={formData.employerLink} onChange={handleInputChange} placeholder="https://volvo.se/soka_jobb" className="mb-4 p-2 border border-gray-600 rounded-md w-full bg-gray-700 text-white" />
                                
                                <Button type="submit" className="mt-4 w-full bg-gray-200 text-black py-2 rounded-md hover:bg-blue-700">Skapa</Button>
                            </form>
                        </CardContent>
                    </Card>
                    
                    <Card className="w-full md:w-2/5 lg:w-1/3 bg-gray-800 rounded-lg overflow-hidden shadow-xl transition-shadow duration-300 hover:shadow-2xl">
                        <CardHeader className="p-6 bg-gray-700 border-b border-gray-600">
                            <CardTitle className="text-2xl font-bold text-white">Ditt Personliga Brev</CardTitle>
                            <CardDescription className="text-gray-400">Här kommer ditt personliga brev vara.</CardDescription>
                        </CardHeader>
                        <CardContent className="p-6">
                            <div className="w-full mx-auto p-4 border border-gray-600 rounded-lg bg-gray-700">
                                {data && data.output && (
                                    <div className="my-5 p-4 bg-gray-800 border border-gray-600 rounded-md shadow-sm text-gray-200">
                                        {data.output}
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </section>
                <section className="container mx-auto py-10 px-6 flex justify-center items-center">
                    <button onClick={() => console.log('Test button clicked')}>Test</button>
                    <iframe
                        src="http://localhost:8501"
                        className="w-[70%] h-[500px] border-none rounded-lg shadow-lg"
                        title="Job Explorer Dashboard"
                    ></iframe>
                </section>
            </div>
        </main>
    );
};

export default Home;
