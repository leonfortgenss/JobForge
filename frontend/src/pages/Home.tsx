import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";

export default function Home() {

    const [formData, setFormData] = useState({
        name: '',
        age: '',
        traits: '',
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [id]: value
        }));
        console.log("formdata", formData)
    };

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
                throw new Error('Error fetching your personal letters');
            }
            return response.json();
        },
    });

    const mutation = useMutation({
        mutationFn: async (formData: { name: string; age: string; traits: string }) => {
            return await fetch('http://127.0.0.1:8000/api/v1/application-creator/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
        },
    });
    

    const handleSubmit = (event: any) => {
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
        <>
            <main className="">
                <section className="flex">
                <Card className="mt-10 w-1/3 ml-10">
                        <CardHeader>
                            <CardTitle>Skapa Personligt Brev</CardTitle>
                            <CardDescription>Skapa ett helt personligt brev med ett klick.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleSubmit}>
                                <Label htmlFor="name">Namn:</Label>
                                <Input id="name" value={formData.name} onChange={handleInputChange} placeholder="Markus Oskarsson" className="mb-4" />

                                <Label htmlFor="age">Ålder:</Label>
                                <Input id="age" value={formData.age} onChange={handleInputChange} placeholder="21" className="mb-4" />

                                <Label htmlFor="traits">Egenskaper:</Label>
                                <Input id="traits" value={formData.traits} onChange={handleInputChange} placeholder="Positiv, Tar Initiativ, Hjälpsam etc" className="mb-4" />

                                <Button type="submit" className="mt-4">Skapa</Button>
                            </form>
                        </CardContent>
                    </Card>
                    <Card className="w-1/2 mt-10 ml-10">
                        <CardHeader>
                            <CardTitle>Ditt Personliga Brev</CardTitle>
                            <CardDescription>Här kommer ditt personliga brev vara.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="w-11/12 h-64 overflow-y-scroll border border-gray-200 rounded-lg p-4">
                                <ul>
                                    {data && data.map((letter: any) => (
                                        <li key={letter.id} className="my-5">
                                            {letter._output}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </CardContent>
                    </Card>
                </section>
            </main>
        </>
    );
}
