import * as React from 'react';
import {
    Filter,
    ReferenceInput,
    SelectInput
} from 'react-admin';


export const LighthouseResultsFilter = props => (
    <Filter {...props}>
        <ReferenceInput label="Website" source="url" reference="lighthouse">
            <SelectInput optionText="url" />
        </ReferenceInput>
        
    </Filter>
);