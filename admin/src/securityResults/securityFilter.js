import * as React from 'react';
import {
    Filter,
    ReferenceInput,
    SelectInput
} from 'react-admin';


export const SecurityResultsFilter = props => (
    <Filter {...props}>
        <ReferenceInput label="Website" source="url" reference="security">
            <SelectInput optionText="url" />
        </ReferenceInput>
        
    </Filter>
);