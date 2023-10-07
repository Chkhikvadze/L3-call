import Textarea from '@l3-lib/ui-core/dist/Textarea'
import Typography from '@l3-lib/ui-core/dist/Typography'

import FormikTextField from 'components/TextFieldFormik'
import {
  StyledForm,
  StyledInputWrapper,
  StyledRoot,
  StyledTextareaWrapper,
} from 'pages/Agents/AgentForm/AgentForm'
import TypographyPrimary from 'components/Typography/Primary'

const GroupForm = ({ formik }: { formik: any }) => {
  const { values, setFieldValue } = formik
  const { group_description } = values

  const onDescriptionChange = (value: string) => {
    setFieldValue('group_description', value)
  }

  return (
    <StyledRoot>
      <StyledForm>
        <StyledInputWrapper>
          <FormikTextField name='group_name' placeholder='Name' label='Name' />

          <StyledTextareaWrapper>
            <TypographyPrimary
              value='Description'
              type={Typography.types.LABEL}
              size={Typography.sizes.md}
            />
            <Textarea
              hint=''
              placeholder='Description'
              name='group_description'
              value={group_description}
              onChange={onDescriptionChange}
            />
          </StyledTextareaWrapper>
        </StyledInputWrapper>
      </StyledForm>
    </StyledRoot>
  )
}

export default GroupForm
