import * as React from "react";
import { SimpleShowLayout, Show, TextField } from 'react-admin';
import { Table, TableBody, TableRow, TableCell, TableHead } from '@material-ui/core';


const TagsField = ({ record }) => {

    if (record.type_audit == "HEADERS") {
        const results = JSON.parse(record.result.replaceAll("'", '"'))
        return (
            <div>
                {Object.keys(results).map((key) => (
                    <div>
                        { results[key]["count"] > 0 ?
                            (<>
                                <h3>{key}</h3>
                                <ul key={key}>
                                    {results[key]["values"].map((value) => (
                                        <li>{value}</li>
                                    ))}
                                </ul>
                            </>) : (<></>)
                        }

                    </div>
                ))}
            </div>
        )
    } else if (record.type_audit == "IMAGES") {
        const results = JSON.parse(record.result.replaceAll("'", '"').replaceAll("None", '"None"'))
        return (
            <div class="table-responsive">
                <Table>
                    <TableHead class="thead-dark">
                        <TableRow>
                            <TableCell scope="col">Image</TableCell>
                            <TableCell scope="col">Title</TableCell>
                            <TableCell scope="col">Alt</TableCell>

                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {results["images"].map(item => (
                            <TableRow>
                            <TableCell>
                                <a href={item.url}>
                                    <img class="img-exTableRowact" style={{width:'100%', 'max-width':'40px'}} src={item.url} />
                                </a>
                            </TableCell>
                            <TableCell>
                                {item.title}
                            </TableCell>
                            <TableCell>
                                {item.alt}
                            </TableCell>

                        </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        )
    } else if (record.type_audit == "LINKS") {
        const results = JSON.parse(record.result.replaceAll("'", '"').replaceAll("None", '"None"'))
        console.log(results)
        return (
            <div class="table-responsive">
            {Object.keys(results).map(key => (
                
                <Table size="small">
                    <TableHead class="thead-dark">
                        <TableRow>
                            <TableCell scope="col"><h2> Status Code: {key}</h2></TableCell>
                            

                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {results[key].map(item => (
                            <TableRow>
                            <TableCell>
                                <a href={item}>
                                    {item}
                                </a>
                            </TableCell>
                           

                        </TableRow>
                        ))}
                    </TableBody>
                </Table>
               
            
            ))}
            </div>
        )
    }

}

export const ExtractorShow = (props) => (
    <Show {...props}>
        <SimpleShowLayout>
            <TextField source="url" />
            <TextField source="type_audit" />
            <TagsField source="result" />
        </SimpleShowLayout>
    </Show>
);
