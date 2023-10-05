import TypographyPrimary from 'components/Typography/Primary'
import TypographySecondary from 'components/Typography/Secondary'
import MemberText from 'modals/AIChatModal/components/ChatMembers/components/MemberText'
import styled from 'styled-components'

import Typography from '@l3-lib/ui-core/dist/Typography'

const TempCard = ({ name, description }: { name: string; description: string }) => {
  return (
    <StyledCard>
      {/* <MemberText name={name} role={description} /> */}

      <TypographyPrimary value={name} size={Typography.sizes.lg} />

      <TypographySecondary value={description} size={Typography.sizes.md} />
    </StyledCard>
  )
}

export default TempCard

const StyledCard = styled.div`
  width: 200px;
  min-width: 200px;
  height: 100px;
  min-height: 100px;

  padding: 0px 20px;

  background: ${({ theme }) => theme.body.cardBgColor};
  border: ${({ theme }) => theme.body.border};
  border-radius: 8px;

  display: flex;
  flex-direction: column;

  justify-content: center;
`
