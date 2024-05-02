import { Button } from "@/components/ui/button";
import { useMutation, useQuery } from "@tanstack/react-query";


export default function Home() {
    const { data, error, isLoading, isError } = useQuery({
        queryKey: ['_output'], 
        queryFn: async () => {
            const response = await fetch('http://127.0.0.1:8000/api/v1/application-creator/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            if (!response.ok) {
                throw new Error('Error fetching your personal letters');
            }
            return response.json();
        }
    });
    // @ts-ignore
    const mutation = useMutation({
        mutationFn: async () => {
            return await fetch('http://127.0.0.1:8000/api/v1/application-creator/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', 
                },
                body: JSON.stringify({
                    "_input": "My name is Leon, I am happy, determined, lots of experience"
                }),
            });
        }
    });

    if (isLoading) {
        return <div>Loading...</div>;
    }
    
    if (isError) {
        return <div>Error: {error.message}</div>;
    }

    return(
        <>
            <div className="my-2 mt-5">
            <Button onClick={() => { console.log("Button clicked"); mutation.mutate(); }}>
                Submit
            </Button>
            </div>
            <ul className="w-[80vw] mx-auto">
                {data && data.map((letter: any) => (
                    <li key={letter.id} className="my-5">
                        {letter._output}
                    </li>
                ))}
            </ul>
        </>
    );
}


