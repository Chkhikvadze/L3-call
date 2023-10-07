import Textarea from '@l3-lib/ui-core/dist/Textarea'
import Typography from '@l3-lib/ui-core/dist/Typography'

import { FormikProvider } from 'formik'

import FormikTextField from 'components/TextFieldFormik'
import {
  StyledForm,
  StyledInputWrapper,
  StyledRoot,
  StyledTextareaWrapper,
} from 'pages/Agents/AgentForm/AgentForm'
import TypographyPrimary from 'components/Typography/Primary'
import { useCreateContact } from '../useCreateContract'
import AgentDropdown from 'pages/Agents/AgentForm/components/AgentDropdown'
import { useContactForm } from './useContactForm'

const ContactForm = ({ formik }: { formik: any }) => {
  const { groupOptions } = useContactForm()

  const { values, setFieldValue } = formik
  const { contact_description, contact_group_id } = values

  const onDescriptionChange = (value: string) => {
    setFieldValue('contact_description', value)
  }

  return (
    <StyledRoot>
      <StyledForm>
        <StyledInputWrapper>
          <FormikTextField name='contact_name' placeholder='Name' label='Name' size='small' />

          <StyledTextareaWrapper>
            <TypographyPrimary
              value='Description'
              type={Typography.types.LABEL}
              size={Typography.sizes.md}
            />

            <Textarea
              hint=''
              placeholder='Description'
              name='contact_description'
              value={contact_description}
              onChange={onDescriptionChange}
            />
          </StyledTextareaWrapper>

          <FormikTextField name='contact_phone' placeholder='Phone' label='Phone' size='small' />

          <FormikTextField name='contact_email' placeholder='Email' label='Email' size='small' />

          <AgentDropdown
            label={'Group'}
            fieldName={'contact_group_id'}
            setFieldValue={setFieldValue}
            fieldValue={contact_group_id}
            options={groupOptions}
            optionSize={'small'}
          />
        </StyledInputWrapper>
      </StyledForm>
    </StyledRoot>
  )
}

export default ContactForm
