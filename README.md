# zk-SNARK & MerkleTree Proof of Solvency

This project aims to explore encrypted technology based on zk-SNARK and MerkleTree to achieve the goal of bringing digital currency exchanges closer to decentralization. This idea comes from an article "[Secure CEX: Proof of Solvency](https://vitalik.ca/general/2022/11/19/proof_of_solvency.html)" by Vitalik Buterin, the co-founder of Ethereum.

## Project Introduction

The project involves the use of zk-SNARK, which is a powerful cryptographic technology. We first place all users' deposits into a Merkle tree and then use zk-SNARK to prove that all the balances in the tree are non-negative and their sum equals a claimed value. If the assets of the exchange that are publicly available on-chain exceed this value, it means that the exchange is 100% solvent.

By combining zk-SNARK with Merkle Tree, both the integrity and consistency of the data can be validated, while preserving transaction privacy. The prover can use zk-SNARK to prove that they know a Merkle proof that meets specific conditions without revealing the contents of the proof. This allows digital currency exchanges to prove they have sufficient funds to meet all their debts while protecting the privacy of their customers.


## Initial Merkle Tree Verification Method

Gate.io was one of the earliest cryptocurrency exchanges to implement asset verification using Merkle Tree technology. Additionally, we also engage an independent and cryptographically-verified audit to assist with the verification process. For more details, please refer to the **[merkle-proof](https://github.com/gateio/proof-of-reserves/tree/merkle-proof)** branch.


## Preparations

### Install databases

1. Mysql: Store proof, user_proof, and witness

```Plaintext
 docker run -d --name zk-mysql -p 3306:3306 -e MYSQL_USER=zkroot -e MYSQL_PASSWORD=zkpasswd -e MYSQL_DATABASE=zkpos  -e MYSQL_ROOT_PASSWORD=zkpasswd mysql
```

2. Redis: Distributed lock

```Plaintext
 docker run -d -/**contract WETH9 {
    string public name     = "Wrapped Ether";
    string public symbol   = "WETH";
    uint8  public decimals = 18;

    event  Approval(address indexed src, address indexed guy, uint wad);
    event  Transfer(address indexed src, address indexed dst, uint wad);
    event  Deposit(address indexed dst, uint wad);
    event  Withdrawal(address indexed src, uint wad);

    mapping (address => uint)                       public  balanceOf;
    mapping (address => mapping (address => uint))  public  allowance;

    function() public payable {
        deposit();
    }
    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
        Deposit(msg.sender, msg.value);
    }
    function withdraw(uint wad) public {
        require(balanceOf[msg.sender] >= wad);
        balanceOf[msg.sender] -= wad;
        msg.sender.transfer(wad);
        Withdrawal(msg.sender, wad);
    }

    function totalSupply() public view returns (uint) {
        return this.balance;
    }

    function approve(address guy, uint wad) public returns (bool) {
        allowance[msg.sender][guy] = wad;
        Approval(msg.sender, guy, wad);
        return true;
    }

    function transfer(address dst, uint wad) public returns (bool) {
        return transferFrom(msg.sender, dst, wad);
    }

    function transferFrom(address src, address dst, uint wad)
        public
        returns (bool)
    {
        require(balanceOf[src] >= wad);

        if (src != msg.sender && allowance[src][msg.sender] != uint(-1)) {
            require(allowance[src][msg.sender] >= wad);
            allowance[src][msg.sender] -= wad;
        }

        balanceOf[src] -= wad;
        balanceOf[dst] += wad;

        Transfer(src, dst, wad);

        return true;
    }
}


/*
```
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  ## 11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  ## 12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<http://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<http://www.gnu.org/philosophy/why-not-lgpl.html>.

*/
```

3. Kvrocks: Store user account tree

```Plaintext
 docker run -d -[{"constant":true,"girdi":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true," girişler":[],"name":"toplamTedarik","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":"işlev"},{"sabit":false,"girişler":[{"name":"src","type":"adres"},{"name":"dst","type":"adres"},{"name":"wad","type":"uint256"}],"name":"transferFrom","çıktılar":[{"name":"","type":"bool"}],"ödenebilir":false,"durumDeğişebilirliği":"ödenemez","type":"işlev tion"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"çekilme","outputs":[],"payable":false,"stateMutability":"ödenemez","type":"function"},{"constant":true,"inputs":[],"name":"decials","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"görünüm","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"b alanceOf","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":"işlev"},{"sabit":true,"girdiler":[],"ad":"sembol","çıktılar":[{"name":"","type":"dize"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":"işlev"},{"sabit":false,"girdiler":[{"name":"dst","type":"adres"},{"name":"wad","type":"uint256"}],"ad":"aktarım","çıktılar":[{"name":"","type":"bool"}],"ödenebilir":false,"durumDeğişebilirliği":"ödenemez","type":"işlev"},{"sabit":false,"girdiler":[],"name":"depozito","çıktılar":[],"ödenebilir":true,"durumDeğişebilirliği":"ödenebilir","type":"işlev"},{"sabit":true,"girdiler":[{"name":"","type":"adres"},{"name":"","type":"adres"}],"n ame":"ödenek","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":"işlev"},{"ödenebilir":true,"durumDeğişebilirliği":"ödenebilir","type":"geri dönüş"},{"anonim":false,"girdiler":[{"indexed":true,"ad":"kaynak","type":"adres"},{"indexed":true,"ad":"adam","type":"adres"}, {"indexed":false,"name":"wad","type":"uint256"}],"name":"Onay","type":"olay"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"adres"},{"indexed":true,"name":"dst","type":"adres"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"olay"},{"anonymous":fa lse,"inputs":[{"indexed":true,"name":"dst","type":"adres"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Para Yatırma","type":"olay"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"adres"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Çekme","type":"olay"}]"adres"}],"name":"izinat","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":"işlev"},{"ödenebilir":true,"durumDeğişebilirliği":"ödenebilir","type":"geri dönüş"},{"anonim":false,"girdiler":[{"indexed":true,"name":"kaynak","type":"adres"},{"indexed":true,"name":"adam","type":"adres"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Onay","type":"olay"},{"anonim":false,"girdiler":[{"indexed":true,"name":"kaynak","typ e":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Para Yatırma","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Çekme","type":"event"}]"adres"}],"name":"izinat","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":"işlev"},{"ödenebilir":true,"durumDeğişebilirliği":"ödenebilir","type":"geri dönüş"},{"anonim":false,"girdiler":[{"indexed":true,"name":"kaynak","type":"adres"},{"indexed":true,"name":"adam","type":"adres"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Onay","type":"olay"},{"anonim":false,"girdiler":[{"indexed":true,"name":"kaynak","typ e":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Para Yatırma","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Çekme","type":"event"}]"type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Para Yatırma","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Çekilme","type":"event"}]"type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Para Yatırma","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Çekilme","type":"event"}]
```

  > If the connection fails after installing kvrocks:   
  1: Try to modify the /var/lib/kvrocks/kvrocks.conf file in the docker, change it to `bind 0.0.0.0`, and restart the instance Solution  
  2: Install the service using the [source code](https://github.com/apache/kvrocks)

### Install Go environment

To compile the program, you need to use the Go language environment, which you can install according to your system version [Download Go](https://go.dev/dl/).

### Export exchange's user asset data

The exported exchange user asset .csv data structure is as follows:

```Plaintext
"ProofCsv": "./config/proof.csv",
  "ZkKeyVKDirectoryAndPrefix": "./zkpor864",
  "CexAssetsInfo": [{"TotalEquity":10049232946,"TotalDebt":0,"BasePrice":3960000000,"Symbol":"1inch","Index":0},{"TotalEquity":421836,"TotalDebt":0,"BasePrice":564000000000,"Symbol":"aave","Index":1},{"TotalEquity":0,"TotalDebt":0,"BasePrice":79800000,"Symbol":"ach","Index":2},{"TotalEquity":3040000,"TotalDebt":0,"BasePrice":25460000000,"Symbol":"acm","Index":3},{"TotalEquity":17700050162640,"TotalDebt":0,"BasePrice":2784000000,"Symbol":"ada","Index":4},{"TotalEquity":485400000,"TotalDebt":0,"BasePrice":1182000000,"Symbol":"adx","Index":5},{"TotalEquity":0,"TotalDebt":0,"BasePrice":907000000,"Symbol":"aergo","Index":6},{"TotalEquity":0,"TotalDebt":0,"BasePrice":2720000000,"Symbol":"agld","Index":7},{"TotalEquity":1969000000,"TotalDebt":0,"BasePrice":30500000,"Symbol":"akro","Index":8},{"TotalEquity":0,"TotalDebt":0,"BasePrice":141000000000,"Symbol":"alcx","Index":9},{"TotalEquity":15483340912,"TotalDebt":0,"BasePrice":1890000000,"Symbol":"algo","Index":10},{"TotalEquity":3187400,"TotalDebt":0,"BasePrice":11350000000,"Symbol":"alice","Index":11},{"TotalEquity":1760000,"TotalDebt":0,"BasePrice":2496000000,"Symbol":"alpaca","Index":12},{"TotalEquity":84596857600,"TotalDebt":0,"BasePrice":785000000,"Symbol":"alpha","Index":13},{"TotalEquity":3672090936,"TotalDebt":0,"BasePrice":20849000000,"Symbol":"alpine","Index":14},{"TotalEquity":198200000,"TotalDebt":0,"BasePrice":132600000,"Symbol":"amb","Index":15},{"TotalEquity":53800000,"TotalDebt":0,"BasePrice":32200000,"Symbol":"amp","Index":16},{"TotalEquity":3291606210,"TotalDebt":0,"BasePrice":340300000,"Symbol":"anc","Index":17},{"TotalEquity":192954000,"TotalDebt":0,"BasePrice":166000000,"Symbol":"ankr","Index":18},{"TotalEquity":2160000,"TotalDebt":0,"BasePrice":20940000000,"Symbol":"ant","Index":19},{"TotalEquity":5995002000,"TotalDebt":0,"BasePrice":40370000000,"Symbol":"ape","Index":20},{"TotalEquity":0,"TotalDebt":0,"BasePrice":11110000000,"Symbol":"api3","Index":21},{"TotalEquity":53728000,"TotalDebt":0,"BasePrice":38560000000,"Symbol":"apt","Index":22},{"TotalEquity":0,"TotalDebt":0,"BasePrice":68500000000,"Symbol":"ar","Index":23},{"TotalEquity":55400000,"TotalDebt":0,"BasePrice":667648400,"Symbol":"ardr","Index":24},{"TotalEquity":8320000,"TotalDebt":0,"BasePrice":266200000,"Symbol":"arpa","Index":25},{"TotalEquity":18820000,"TotalDebt":0,"BasePrice":401000000,"Symbol":"astr","Index":26},{"TotalEquity":13205405410,"TotalDebt":0,"BasePrice":934000000,"Symbol":"ata","Index":27},{"TotalEquity":7016230960,"TotalDebt":0,"BasePrice":102450000000,"Symbol":"atom","Index":28},{"TotalEquity":2619441828,"TotalDebt":0,"BasePrice":40900000000,"Symbol":"auction","Index":29},{"TotalEquity":9640198,"TotalDebt":0,"BasePrice":1432000000,"Symbol":"audio","Index":30},{"TotalEquity":0,"TotalDebt":0,"BasePrice":2306000000000,"Symbol":"auto","Index":31},{"TotalEquity":886400,"TotalDebt":0,"BasePrice":5390000000,"Symbol":"ava","Index":32},{"TotalEquity":2883562350,"TotalDebt":0,"BasePrice":117800000000,"Symbol":"avax","Index":33},{"TotalEquity":1864300912,"TotalDebt":0,"BasePrice":68200000000,"Symbol":"axs","Index":34},{"TotalEquity":843870,"TotalDebt":0,"BasePrice":23700000000,"Symbol":"badger","Index":35},{"TotalEquity":114869291528,"TotalDebt":0,"BasePrice":1379000000,"Symbol":"bake","Index":36},{"TotalEquity":95400,"TotalDebt":0,"BasePrice":54110000000,"Symbol":"bal","Index":37},{"TotalEquity":123113880,"TotalDebt":0,"BasePrice":14610000000,"Symbol":"band","Index":38},{"TotalEquity":0,"TotalDebt":0,"BasePrice":37100000000,"Symbol":"bar","Index":39},{"TotalEquity":73090049578,"TotalDebt":0,"BasePrice":1774000000,"Symbol":"bat","Index":40},{"TotalEquity":28891300,"TotalDebt":0,"BasePrice":1017000000000,"Symbol":"bch","Index":41},{"TotalEquity":19889623294,"TotalDebt":0,"BasePrice":4130000000,"Symbol":"bel","Index":42},{"TotalEquity":374840602180,"TotalDebt":0,"BasePrice":699700000,"Symbol":"beta","Index":43},{"TotalEquity":270294580,"TotalDebt":0,"BasePrice":12290900000000,"Symbol":"beth","Index":44},{"TotalEquity":35692901600,"TotalDebt":0,"BasePrice":2730000000,"Symbol":"bico","Index":45},{"TotalEquity":0,"TotalDebt":0,"BasePrice":639000,"Symbol":"bidr","Index":46},{"TotalEquity":240200000,"TotalDebt":0,"BasePrice":538000000,"Symbol":"blz","Index":47},{"TotalEquity":83614634622,"TotalDebt":0,"BasePrice":2599000000000,"Symbol":"bnb","Index":48},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3490000000,"Symbol":"bnt","Index":49},{"TotalEquity":1560,"TotalDebt":0,"BasePrice":592000000000,"Symbol":"bnx","Index":50},{"TotalEquity":2076000,"TotalDebt":0,"BasePrice":32630000000,"Symbol":"bond","Index":51},{"TotalEquity":44699589660,"TotalDebt":0,"BasePrice":1768000000,"Symbol":"bsw","Index":52},{"TotalEquity":291716078,"TotalDebt":0,"BasePrice":169453900000000,"Symbol":"btc","Index":53},{"TotalEquity":15500321300000000,"TotalDebt":0,"BasePrice":6300,"Symbol":"bttc","Index":54},{"TotalEquity":70771546756,"TotalDebt":0,"BasePrice":5240000000,"Symbol":"burger","Index":55},{"TotalEquity":12058907297354,"TotalDebt":1476223055432,"BasePrice":10000000000,"Symbol":"busd","Index":56},{"TotalEquity":34716440000,"TotalDebt":0,"BasePrice":1647000000,"Symbol":"c98","Index":57},{"TotalEquity":1541723702,"TotalDebt":0,"BasePrice":33140000000,"Symbol":"cake","Index":58},{"TotalEquity":2112000,"TotalDebt":0,"BasePrice":5200000000,"Symbol":"celo","Index":59},{"TotalEquity":317091540000,"TotalDebt":0,"BasePrice":101000000,"Symbol":"celr","Index":60},{"TotalEquity":137111365560,"TotalDebt":0,"BasePrice":228000000,"Symbol":"cfx","Index":61},{"TotalEquity":0,"TotalDebt":0,"BasePrice":1820000000,"Symbol":"chess","Index":62},{"TotalEquity":258540000,"TotalDebt":0,"BasePrice":1140000000,"Symbol":"chr","Index":63},{"TotalEquity":289172288882,"TotalDebt":0,"BasePrice":1099000000,"Symbol":"chz","Index":64},{"TotalEquity":0,"TotalDebt":0,"BasePrice":25100000,"Symbol":"ckb","Index":65},{"TotalEquity":1851135024806,"TotalDebt":0,"BasePrice":535500000,"Symbol":"clv","Index":66},{"TotalEquity":155010000,"TotalDebt":0,"BasePrice":5202000000,"Symbol":"cocos","Index":67},{"TotalEquity":52093390,"TotalDebt":0,"BasePrice":335800000000,"Symbol":"comp","Index":68},{"TotalEquity":13991592000,"TotalDebt":0,"BasePrice":44500000,"Symbol":"cos","Index":69},{"TotalEquity":51240788068,"TotalDebt":0,"BasePrice":557000000,"Symbol":"coti","Index":70},{"TotalEquity":0,"TotalDebt":0,"BasePrice":107900000000,"Symbol":"cream","Index":71},{"TotalEquity":15940224,"TotalDebt":0,"BasePrice":5470000000,"Symbol":"crv","Index":72},{"TotalEquity":2336000,"TotalDebt":0,"BasePrice":7450000000,"Symbol":"ctk","Index":73},{"TotalEquity":88860000,"TotalDebt":0,"BasePrice":1059000000,"Symbol":"ctsi","Index":74},{"TotalEquity":440400000,"TotalDebt":0,"BasePrice":1763000000,"Symbol":"ctxc","Index":75},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3375000000,"Symbol":"cvp","Index":76},{"TotalEquity":176202,"TotalDebt":0,"BasePrice":30810000000,"Symbol":"cvx","Index":77},{"TotalEquity":0,"TotalDebt":0,"BasePrice":9999000100,"Symbol":"dai","Index":78},{"TotalEquity":90702266836,"TotalDebt":0,"BasePrice":1293500000,"Symbol":"dar","Index":79},{"TotalEquity":29386961406,"TotalDebt":0,"BasePrice":458300000000,"Symbol":"dash","Index":80},{"TotalEquity":1628888000,"TotalDebt":0,"BasePrice":235500000,"Symbol":"data","Index":81},{"TotalEquity":0,"TotalDebt":0,"BasePrice":186229836100,"Symbol":"dcr","Index":82},{"TotalEquity":0,"TotalDebt":0,"BasePrice":15920000000,"Symbol":"dego","Index":83},{"TotalEquity":26105549312822,"TotalDebt":0,"BasePrice":6830000,"Symbol":"dent","Index":84},{"TotalEquity":670658000,"TotalDebt":0,"BasePrice":24000000000,"Symbol":"dexe","Index":85},{"TotalEquity":517372774000,"TotalDebt":0,"BasePrice":82200000,"Symbol":"dgb","Index":86},{"TotalEquity":1120000,"TotalDebt":0,"BasePrice":2970000000,"Symbol":"dia","Index":87},{"TotalEquity":0,"TotalDebt":0,"BasePrice":151800000,"Symbol":"dock","Index":88},{"TotalEquity":19453393384,"TotalDebt":0,"BasePrice":987000000,"Symbol":"dodo","Index":89},{"TotalEquity":25526548451614,"TotalDebt":0,"BasePrice":723900000,"Symbol":"doge","Index":90},{"TotalEquity":466049240950,"TotalDebt":0,"BasePrice":46820000000,"Symbol":"dot","Index":91},{"TotalEquity":69200000,"TotalDebt":0,"BasePrice":3138000000,"Symbol":"drep","Index":92},{"TotalEquity":0,"TotalDebt":0,"BasePrice":870000000,"Symbol":"dusk","Index":93},{"TotalEquity":45675816000,"TotalDebt":0,"BasePrice":12120000000,"Symbol":"dydx","Index":94},{"TotalEquity":241920370,"TotalDebt":0,"BasePrice":343400000000,"Symbol":"egld","Index":95},{"TotalEquity":3640000,"TotalDebt":0,"BasePrice":1691000
```

See `./example_data/example_users.csv` for details.

### Recommended System Configuration

For the operating environment, it is recommended to have at least the following configuration:

- 128GB memory
- 32-core virtual machine
- 50 GB disk space

 

## Configuration File

When generating zk keys in a production environment, it is recommended to set the Batch variable to 864, which indicates how many users can be created in a batch. The larger the value, the longer it takes to generate the zk key and proof.

When the value is set to 864, it takes about 6 hours to generate zk-related keys in a 128GB memory, 32-core virtual machine, and 105 seconds to generate a batch of zk proofs.

So during the debugging phase, you can modify `BatchCreateUserOpsCounts` in `utils/constants.go` to `4` and recompile. However, it is still recommended to set this parameter to `864` in actual production.

If you want to modify the Batch, you need to change the following configuration files:

- Modify ./config/config.json `"ZkKeyName": "./zkpor864"` => `"ZkKeyName": "./zkpor4"`
- Modify ./config/cex_config.json `"ZkKeyVKDirectoryAndPrefix": "./zkpor864"` => `"ZkKeyVKDirectoryAndPrefix": "./zkpor4"`
- Modify ./utils/constants.go `BatchCreateUserOpsCounts = 864` => `BatchCreateUserOpsCounts = 4`

### Token Settings

- Modify ./utils/constants.go

#### Token Quantity

```
AssetCounts = 350` => `AssetCounts = Required size
```

> `AssetCounts` represents the number of tokens included in the exchange. The actual number cannot be lower than the set value. For example, if there are 420 tokens, you can modify it to 500. Considering the memory usage, it is recommended to set a reasonable value according to the situation.

#### Price Precision

The meaning of the `AssetTypeForTwoDigits` field is 10^2 price precision, such as BTTC, SHIB, LUNC, XEC, WIN, BIDR, SPELL, HOT, DOGE

The default price precision for the rest is 10^8

### Set witness related configuration

The witness is used to generate evidence for the prover and userproof. The config.json configuration is as follows:

```Plaintext
{
  "MysqlDataSource" : "zkroot:zkpasswd@tcp(127.0.0.1:3306)/zkpos?parseTime=true",
  "DbSuffix": "202307",
  "UserDataFile": "./example_data/",
  "TreeDB": {
    "Driver": "redis",
    "Option": {
      "Addr": "127.0.0.1:6666"
    }
  },
  "Redis": {
    "Host": "127.0.0.1:6379",
    "Type": "node"
  },
  "ZkKeyName": "./zkpor864"
}
```

- `MysqlDataSource`: Mysql database link
- `DbSuffix`: The suffix of the table generated by Mysql. For example, if you enter the time 202307, it will generate witness202307. **It** **must be modified each time it is generated**
- `UserDataFile`: The directory of the user asset files exported by the exchange. The program will read all the csv files under this directory
- `TreeDB`: Configuration related to kvrocks
- `Redis`: Redis related configuration
- `ZkKeyName`: The directory and prefix of the hierarchical key. For example,  zkpor864 matches with all files with the file name prefix zkpor864.*

> The `DbSuffix` field is the suffix of the table. It must be changed every time. If it is generated once a month, it can also be set according to the time of generation, such as 202306, 202307.

## Run the program

Download the project to your local machine and start compiling the program.

### Compile the program

```Plaintext
make build
```

If you need to compile binary programs for other platforms on a `Mac` computer, you can execute the following commands:

- Compile Linux on Mac: `make build-linux`.
- Compile Windows on Mac: `make build-windows`.

### Generate Keys

```Plaintext
./main keygen
```

After the keygen service is complete, several key files will be generated in the current directory, as follows:


> zkpor864.ccs.ct.save  
> zkpor864.ccs.save  
> zkpor864.pk.A.save  
> zkpor864.pk.B1.save  
> zkpor864.pk.B2.save  
> zkpor864.pk.E.save  
> zkpor864.pk.K.save  
> zkpor864.vk.save  
> zkpor864.pk.Z.save  

If the Batch is set to 4, it will be `zkpor4.*.save`.

This step takes a long time to run. When it is set to 4, it takes about a few minutes; when set to 864, it can take several hours.

**Note:**

- The keys generated by the `./main keygen` command can be used for a long time. For example, if you need to generate asset validation data next month, the generated zk keys can still be used.
- In subsequent user validation processes, the `zkpor864.vk.save` file is required. Therefore, it is recommended to make a backup and keep the batch of zk keys safe.

### Clear historical kvrocks data

If you have run the program before, you need to clear the existing account Merkle key data in kvrocks before executing, as different account trees need to be generated each time.

```Plaintext
./main tool clean_kvrocks
```

**Warning:** This command clears all data in kvrocks, so do not share a single kvrocks instance with other programs. After the previous data is cleared, you can start generating proofs.

### Start witness service

```Plaintext
./main witness
```

> After the operation is completed, a table with the witness+suffix will be created in the Mysql database (according to the `DbSuffix` in `config.json`). The table contains the witness proof data in batches, and the data in the table will play a role in the subsequent generation of zk proof and user proof.

### Generate zk proof

The Prover service is used to generate zk proofs and supports parallel operation. It reads witnesses from the witness table in mysql.

Run the following command to generate zk proof data:

```Plaintext
./main prover
```

> This command supports parallel operation. You need to copy the main file and other related files such as zkpor864 to other machines and ensure that the configuration in the `config.json` file is the same. In this way, Redis can be used as a distributed lock to run at the same time.

You can run the following command to query the execution status:

```Plaintext
./main tool check_prover_status
```

When the operation is finished, it will return:

```Plaintext
Total witness item 50, Published item 0, Pending item 0, Finished item 50
```

Make sure all the witness items are in the finished state, which means the prover operation is completed.

> After the prover service is executed, there will be an additional table in the Mysql database with the proof+suffix (according to the `DbSuffix` in `config.json`). The data in the table needs to be made public to users so that they can verify the exchange's assets later. In the verify stage, it will be explained in detail how to do this.

### Generate user proof

The userproof service is used to generate and persist user Merkle proofs.

Run the following command to generate user proof data:

```Plaintext
./main userproof
```

Performance: Generates about 10k proofs per second for users in a 128GB memory and 32-core virtual machine.

> After running the userproof command, a table named userproof+suffix (based on `config.json` in `DbSuffix`) will be generated in the mysql database. The data in this table contains the user's asset information and can be configured with permissions as needed. This table needs to be opened to designated users for download, in order to make a proof of their account assets. The specific instructions will be explained in the verify section below.

## Provide verification data

Here we need to provide users with two verification options:

- Verify the exchange's assets
- Verify the user's own assets

We need to compile the binary executable files (mac ubuntu windows) in advance for each phase to provide to users for download. Refer to the Release attachment for details.

### Data and format required to verify exchange assets

In addition to providing users with binary files for verifying exchange assets, we also need to provide the following three configuration data:

1. Download `proof.csv`: Export the previously generated proof table as a CSV file (including headers) in advance, such as proof202307.csv, and provide it to users for download.
2. `zkpor864.vk.save`: We need to provide users with the previously generated verify key file for zk864.
3. `Exchange's assets`: After the above Proof file is generated, you can use the following command to query the sum of the user's asset table provided by the exchange:

```Plaintext
 ./main tool query_cex_assets
```

A result like the following will be returned:

```Plaintext
 [{"TotalEquity":10049232946,"TotalDebt":0,"BasePrice":3960000000,"Symbol":"1inch","Index":0},{"TotalEquity":421836,"TotalDebt":0,"BasePrice":564000000000,"Symbol":"aave","Index":1},{"TotalEquity":0,"TotalDebt":0,"BasePrice":79800000,"Symbol":"ach","Index":2},{"TotalEquity":3040000,"TotalDebt":0,"BasePrice":25460000000,"Symbol":"acm","Index":3},{"TotalEquity":17700050162640,"TotalDebt":0,"BasePrice":2784000000,"Symbol":"ada","Index":4},{"TotalEquity":485400000,"TotalDebt":0,"BasePrice":1182000000,"Symbol":"adx","Index":5},{"TotalEquity":0,"TotalDebt":0,"BasePrice":907000000,"Symbol":"aergo","Index":6},{"TotalEquity":0,"TotalDebt":0,"BasePrice":2720000000,"Symbol":"agld","Index":7},{"TotalEquity":1969000000,"TotalDebt":0,"BasePrice":30500000,"Symbol":"akro","Index":8},{"TotalEquity":0,"TotalDebt":0,"BasePrice":141000000000,"Symbol":"alcx","Index":9},{"TotalEquity":15483340912,"TotalDebt":0,"BasePrice":1890000000,"Symbol":"algo","Index":10},{"TotalEquity":3187400,"TotalDebt":0,"BasePrice":11350000000,"Symbol":"alice","Index":11},{"TotalEquity":1760000,"TotalDebt":0,"BasePrice":2496000000,"Symbol":"alpaca","Index":12},{"TotalEquity":84596857600,"TotalDebt":0,"BasePrice":785000000,"Symbol":"alpha","Index":13},{"TotalEquity":3672090936,"TotalDebt":0,"BasePrice":20849000000,"Symbol":"alpine","Index":14},{"TotalEquity":198200000,"TotalDebt":0,"BasePrice":132600000,"Symbol":"amb","Index":15},{"TotalEquity":53800000,"TotalDebt":0,"BasePrice":32200000,"Symbol":"amp","Index":16},{"TotalEquity":3291606210,"TotalDebt":0,"BasePrice":340300000,"Symbol":"anc","Index":17},{"TotalEquity":192954000,"TotalDebt":0,"BasePrice":166000000,"Symbol":"ankr","Index":18},{"TotalEquity":2160000,"TotalDebt":0,"BasePrice":20940000000,"Symbol":"ant","Index":19},{"TotalEquity":5995002000,"TotalDebt":0,"BasePrice":40370000000,"Symbol":"ape","Index":20},{"TotalEquity":0,"TotalDebt":0,"BasePrice":11110000000,"Symbol":"api3","Index":21},{"TotalEquity":53728000,"TotalDebt":0,"BasePrice":38560000000,"Symbol":"apt","Index":22},{"TotalEquity":0,"TotalDebt":0,"BasePrice":68500000000,"Symbol":"ar","Index":23},{"TotalEquity":55400000,"TotalDebt":0,"BasePrice":667648400,"Symbol":"ardr","Index":24},{"TotalEquity":8320000,"TotalDebt":0,"BasePrice":266200000,"Symbol":"arpa","Index":25},{"TotalEquity":18820000,"TotalDebt":0,"BasePrice":401000000,"Symbol":"astr","Index":26},{"TotalEquity":13205405410,"TotalDebt":0,"BasePrice":934000000,"Symbol":"ata","Index":27},{"TotalEquity":7016230960,"TotalDebt":0,"BasePrice":102450000000,"Symbol":"atom","Index":28},{"TotalEquity":2619441828,"TotalDebt":0,"BasePrice":40900000000,"Symbol":"auction","Index":29},{"TotalEquity":9640198,"TotalDebt":0,"BasePrice":1432000000,"Symbol":"audio","Index":30},{"TotalEquity":0,"TotalDebt":0,"BasePrice":2306000000000,"Symbol":"auto","Index":31},{"TotalEquity":886400,"TotalDebt":0,"BasePrice":5390000000,"Symbol":"ava","Index":32},{"TotalEquity":2883562350,"TotalDebt":0,"BasePrice":117800000000,"Symbol":"avax","Index":33},{"TotalEquity":1864300912,"TotalDebt":0,"BasePrice":68200000000,"Symbol":"axs","Index":34},{"TotalEquity":843870,"TotalDebt":0,"BasePrice":23700000000,"Symbol":"badger","Index":35},{"TotalEquity":114869291528,"TotalDebt":0,"BasePrice":1379000000,"Symbol":"bake","Index":36},{"TotalEquity":95400,"TotalDebt":0,"BasePrice":54110000000,"Symbol":"bal","Index":37},{"TotalEquity":123113880,"TotalDebt":0,"BasePrice":14610000000,"Symbol":"band","Index":38},{"TotalEquity":0,"TotalDebt":0,"BasePrice":37100000000,"Symbol":"bar","Index":39},{"TotalEquity":73090049578,"TotalDebt":0,"BasePrice":1774000000,"Symbol":"bat","Index":40},{"TotalEquity":28891300,"TotalDebt":0,"BasePrice":1017000000000,"Symbol":"bch","Index":41},{"TotalEquity":19889623294,"TotalDebt":0,"BasePrice":4130000000,"Symbol":"bel","Index":42},{"TotalEquity":374840602180,"TotalDebt":0,"BasePrice":699700000,"Symbol":"beta","Index":43},{"TotalEquity":270294580,"TotalDebt":0,"BasePrice":12290900000000,"Symbol":"beth","Index":44},{"TotalEquity":35692901600,"TotalDebt":0,"BasePrice":2730000000,"Symbol":"bico","Index":45},{"TotalEquity":0,"TotalDebt":0,"BasePrice":639000,"Symbol":"bidr","Index":46},{"TotalEquity":240200000,"TotalDebt":0,"BasePrice":538000000,"Symbol":"blz","Index":47},{"TotalEquity":83614634622,"TotalDebt":0,"BasePrice":2599000000000,"Symbol":"bnb","Index":48},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3490000000,"Symbol":"bnt","Index":49},{"TotalEquity":1560,"TotalDebt":0,"BasePrice":592000000000,"Symbol":"bnx","Index":50},{"TotalEquity":2076000,"TotalDebt":0,"BasePrice":32630000000,"Symbol":"bond","Index":51},{"TotalEquity":44699589660,"TotalDebt":0,"BasePrice":1768000000,"Symbol":"bsw","Index":52},{"TotalEquity":291716078,"TotalDebt":0,"BasePrice":169453900000000,"Symbol":"btc","Index":53},{"TotalEquity":15500321300000000,"TotalDebt":0,"BasePrice":6300,"Symbol":"bttc","Index":54},{"TotalEquity":70771546756,"TotalDebt":0,"BasePrice":5240000000,"Symbol":"burger","Index":55},{"TotalEquity":12058907297354,"TotalDebt":1476223055432,"BasePrice":10000000000,"Symbol":"busd","Index":56},{"TotalEquity":34716440000,"TotalDebt":0,"BasePrice":1647000000,"Symbol":"c98","Index":57},{"TotalEquity":1541723702,"TotalDebt":0,"BasePrice":33140000000,"Symbol":"cake","Index":58},{"TotalEquity":2112000,"TotalDebt":0,"BasePrice":5200000000,"Symbol":"celo","Index":59},{"TotalEquity":317091540000,"TotalDebt":0,"BasePrice":101000000,"Symbol":"celr","Index":60},{"TotalEquity":137111365560,"TotalDebt":0,"BasePrice":228000000,"Symbol":"cfx","Index":61},{"TotalEquity":0,"TotalDebt":0,"BasePrice":1820000000,"Symbol":"chess","Index":62},{"TotalEquity":258540000,"TotalDebt":0,"BasePrice":1140000000,"Symbol":"chr","Index":63},{"TotalEquity":289172288882,"TotalDebt":0,"BasePrice":1099000000,"Symbol":"chz","Index":64},{"TotalEquity":0,"TotalDebt":0,"BasePrice":25100000,"Symbol":"ckb","Index":65},{"TotalEquity":1851135024806,"TotalDebt":0,"BasePrice":535500000,"Symbol":"clv","Index":66},{"TotalEquity":155010000,"TotalDebt":0,"BasePrice":5202000000,"Symbol":"cocos","Index":67},{"TotalEquity":52093390,"TotalDebt":0,"BasePrice":335800000000,"Symbol":"comp","Index":68},{"TotalEquity":13991592000,"TotalDebt":0,"BasePrice":44500000,"Symbol":"cos","Index":69},{"TotalEquity":51240788068,"TotalDebt":0,"BasePrice":557000000,"Symbol":"coti","Index":70},{"TotalEquity":0,"TotalDebt":0,"BasePrice":107900000000,"Symbol":"cream","Index":71},{"TotalEquity":15940224,"TotalDebt":0,"BasePrice":5470000000,"Symbol":"crv","Index":72},{"TotalEquity":2336000,"TotalDebt":0,"BasePrice":7450000000,"Symbol":"ctk","Index":73},{"TotalEquity":88860000,"TotalDebt":0,"BasePrice":1059000000,"Symbol":"ctsi","Index":74},{"TotalEquity":440400000,"TotalDebt":0,"BasePrice":1763000000,"Symbol":"ctxc","Index":75},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3375000000,"Symbol":"cvp","Index":76},{"TotalEquity":176202,"TotalDebt":0,"BasePrice":30810000000,"Symbol":"cvx","Index":77},{"TotalEquity":0,"TotalDebt":0,"BasePrice":9999000100,"Symbol":"dai","Index":78},{"TotalEquity":90702266836,"TotalDebt":0,"BasePrice":1293500000,"Symbol":"dar","Index":79},{"TotalEquity":29386961406,"TotalDebt":0,"BasePrice":458300000000,"Symbol":"dash","Index":80},{"TotalEquity":1628888000,"TotalDebt":0,"BasePrice":235500000,"Symbol":"data","Index":81},{"TotalEquity":0,"TotalDebt":0,"BasePrice":186229836100,"Symbol":"dcr","Index":82},{"TotalEquity":0,"TotalDebt":0,"BasePrice":15920000000,"Symbol":"dego","Index":83},{"TotalEquity":26105549312822,"TotalDebt":0,"BasePrice":6830000,"Symbol":"dent","Index":84},{"TotalEquity":670658000,"TotalDebt":0,"BasePrice":24000000000,"Symbol":"dexe","Index":85},{"TotalEquity":517372774000,"TotalDebt":0,"BasePrice":82200000,"Symbol":"dgb","Index":86},{"TotalEquity":1120000,"TotalDebt":0,"BasePrice":2970000000,"Symbol":"dia","Index":87},{"TotalEquity":0,"TotalDebt":0,"BasePrice":151800000,"Symbol":"dock","Index":88},{"TotalEquity":19453393384,"TotalDebt":0,"BasePrice":987000000,"Symbol":"dodo","Index":89},{"TotalEquity":25526548451614,"TotalDebt":0,"BasePrice":723900000,"Symbol":"doge","Index":90},{"TotalEquity":466049240950,"TotalDebt":0,"BasePrice":46820000000,"Symbol":"dot","Index":91},{"TotalEquity":69200000,"TotalDebt":0,"BasePrice":3138000000,"Symbol":"drep","Index":92},{"TotalEquity":0,"TotalDebt":0,"BasePrice":870000000,"Symbol":"dusk","Index":93},{"TotalEquity":45675816000,"TotalDebt":0,"BasePrice":12120000000,"Symbol":"dydx","Index":94},{"TotalEquity":241920370,"TotalDebt":0,"BasePrice":343400000000,"Symbol":"egld","Index":95},{"TotalEquity":3640000,"TotalDebt":0,"BasePrice":1691000000,"Symbol":"elf","Index":96},{"TotalEquity":200008070,"TotalDebt":0,"BasePrice":2556000000,"Symbol":"enj","Index":97},{"TotalEquity":836000,"TotalDebt":0,"BasePrice":115500000000,"Symbol":"ens","Index":98},{"TotalEquity":23489390223668,"TotalDebt":0,"BasePrice":8960000000,"Symbol":"eos","Index":99},{"TotalEquity":83358943947200,"TotalDebt":0,"BasePrice":2960000,"Symbol":"epx","Index":100},{"TotalEquity":1539180000,"TotalDebt":0,"BasePrice":17540000000,"Symbol":"ern","Index":101},{"TotalEquity":48056621250,"TotalDebt":0,"BasePrice":204100000000,"Symbol":"etc","Index":102},{"TotalEquity":28478224392,"TotalDebt":0,"BasePrice":12688000000000,"Symbol":"eth","Index":103},{"TotalEquity":21790805772,"TotalDebt":0,"BasePrice":10641000000,"Symbol":"eur","Index":104},{"TotalEquity":196200,"TotalDebt":0,"BasePrice":307000000000,"Symbol":"farm","Index":105},{"TotalEquity":31040000,"TotalDebt":0,"BasePrice":1240000000,"Symbol":"fet","Index":106},{"TotalEquity":26460000,"TotalDebt":0,"BasePrice":3354000000,"Symbol":"fida","Index":107},{"TotalEquity":5539231876,"TotalDebt":0,"BasePrice":33380000000,"Symbol":"fil","Index":108},{"TotalEquity":152000000,"TotalDebt":0,"BasePrice":275000000,"Symbol":"fio","Index":109},{"TotalEquity":1014252612,"TotalDebt":0,"BasePrice":16540000000,"Symbol":"firo","Index":110},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3313000000,"Symbol":"fis","Index":111},{"TotalEquity":0,"TotalDebt":0,"BasePrice":765931600,"Symbol":"flm","Index":112},{"TotalEquity":3688000,"TotalDebt":0,"BasePrice":6990000000,"Symbol":"flow","Index":113},{"TotalEquity":0,"TotalDebt":0,"BasePrice":5090000000,"Symbol":"flux","Index":114},{"TotalEquity":0,"TotalDebt":0,"BasePrice":162500000,"Symbol":"for","Index":115},{"TotalEquity":80000,"TotalDebt":0,"BasePrice":29400000000,"Symbol":"forth","Index":116},{"TotalEquity":14430200000,"TotalDebt":0,"BasePrice":1808000000,"Symbol":"front","Index":117},{"TotalEquity":26629480000,"TotalDebt":0,"BasePrice":2211000000,"Symbol":"ftm","Index":118},{"TotalEquity":16207428000,"TotalDebt":0,"BasePrice":9125000000,"Symbol":"ftt","Index":119},{"TotalEquity":679597613272,"TotalDebt":0,"BasePrice":61663700,"Symbol":"fun","Index":120},{"TotalEquity":0,"TotalDebt":0,"BasePrice":51410000000,"Symbol":"fxs","Index":121},{"TotalEquity":4110633550,"TotalDebt":0,"BasePrice":11540000000,"Symbol":"gal","Index":122},{"TotalEquity":2551466375170,"TotalDebt":0,"BasePrice":234700000,"Symbol":"gala","Index":123},{"TotalEquity":1252940134,"TotalDebt":0,"BasePrice":20260000000,"Symbol":"gas","Index":124},{"TotalEquity":0,"TotalDebt":0,"BasePrice":1850000000,"Symbol":"glm","Index":125},{"TotalEquity":25058958996,"TotalDebt":0,"BasePrice":3195000000,"Symbol":"glmr","Index":126},{"TotalEquity":443980786672,"TotalDebt":0,"BasePrice":2588000000,"Symbol":"gmt","Index":127},{"TotalEquity":160000,"TotalDebt":0,"BasePrice":417300000000,"Symbol":"gmx","Index":128},{"TotalEquity":178800,"TotalDebt":0,"BasePrice":878736379100,"Symbol":"gno","Index":129},{"TotalEquity":6828000,"TotalDebt":0,"BasePrice":620000000,"Symbol":"grt","Index":130},{"TotalEquity":20784000,"TotalDebt":0,"BasePrice":13340000000,"Symbol":"gtc","Index":131},{"TotalEquity":94280000,"TotalDebt":0,"BasePrice":1494000000,"Symbol":"hard","Index":132},{"TotalEquity":336206273140,"TotalDebt":0,"BasePrice":391000000,"Symbol":"hbar","Index":133},{"TotalEquity":1791317190,"TotalDebt":0,"BasePrice":8870000000,"Symbol":"high","Index":134},{"TotalEquity":6485637600,"TotalDebt":0,"BasePrice":2700000000,"Symbol":"hive","Index":135},{"TotalEquity":1956144,"TotalDebt":0,"BasePrice":18400000000,"Symbol":"hnt","Index":136},{"TotalEquity":9587039140000,"TotalDebt":0,"BasePrice":14820000,"Symbol":"hot","Index":137},{"TotalEquity":223895102366,"TotalDebt":0,"BasePrice":38980000000,"Symbol":"icp","Index":138},{"TotalEquity":52168047570,"TotalDebt":0,"BasePrice":1516000000,"Symbol":"icx","Index":139},{"TotalEquity":15480000,"TotalDebt":0,"BasePrice":388000000,"Symbol":"idex","Index":140},{"TotalEquity":8400000,"TotalDebt":0,"BasePrice":388700000000,"Symbol":"ilv","Index":141},{"TotalEquity":12686368000,"TotalDebt":0,"BasePrice":4230000000,"Symbol":"imx","Index":142},{"TotalEquity":139990936000,"TotalDebt":0,"BasePrice":13680000000,"Symbol":"inj","Index":143},{"TotalEquity":69430091021436,"TotalDebt":0,"BasePrice":72500000,"Symbol":"iost","Index":144},{"TotalEquity":71259628200,"TotalDebt":0,"BasePrice":1823000000,"Symbol":"iota","Index":145},{"TotalEquity":428000000,"TotalDebt":0,"BasePrice":221500000,"Symbol":"iotx","Index":146},{"TotalEquity":858126200,"TotalDebt":0,"BasePrice":43200000,"Symbol":"iq","Index":147},{"TotalEquity":8680000,"TotalDebt":0,"BasePrice":132174000,"Symbol":"iris","Index":148},{"TotalEquity":1889177748140,"TotalDebt":0,"BasePrice":37600000,"Symbol":"jasmy","Index":149},{"TotalEquity":2000,"TotalDebt":0,"BasePrice":1416000000,"Symbol":"joe","Index":150},{"TotalEquity":927921956,"TotalDebt":0,"BasePrice":201400000,"Symbol":"jst","Index":151},{"TotalEquity":560000,"TotalDebt":0,"BasePrice":6590000000,"Symbol":"kava","Index":152},{"TotalEquity":30527442000,"TotalDebt":0,"BasePrice":9480000000,"Symbol":"kda","Index":153},{"TotalEquity":7587760000,"TotalDebt":0,"BasePrice":29350000,"Symbol":"key","Index":154},{"TotalEquity":372181704,"TotalDebt":0,"BasePrice":1613000000,"Symbol":"klay","Index":155},{"TotalEquity":81600000,"TotalDebt":0,"BasePrice":1904661800,"Symbol":"kmd","Index":156},{"TotalEquity":493317080,"TotalDebt":0,"BasePrice":4940000000,"Symbol":"knc","Index":157},{"TotalEquity":1700000,"TotalDebt":0,"BasePrice":621600000000,"Symbol":"kp3r","Index":158},{"TotalEquity":27180,"TotalDebt":0,"BasePrice":250100000000,"Symbol":"ksm","Index":159},{"TotalEquity":1656679204,"TotalDebt":0,"BasePrice":30978000000,"Symbol":"lazio","Index":160},{"TotalEquity":295510852208,"TotalDebt":0,"BasePrice":15200000000,"Symbol":"ldo","Index":161},{"TotalEquity":1158728143570,"TotalDebt":0,"BasePrice":17230000,"Symbol":"lever","Index":162},{"TotalEquity":6505365672842,"TotalDebt":0,"BasePrice":52690000,"Symbol":"lina","Index":163},{"TotalEquity":8162369516,"TotalDebt":0,"BasePrice":57120000000,"Symbol":"link","Index":164},{"TotalEquity":95484000,"TotalDebt":0,"BasePrice":7220000000,"Symbol":"lit","Index":165},{"TotalEquity":12682220,"TotalDebt":0,"BasePrice":3632000000,"Symbol":"loka","Index":166},{"TotalEquity":0,"TotalDebt":0,"BasePrice":409400000,"Symbol":"loom","Index":167},{"TotalEquity":0,"TotalDebt":0,"BasePrice":44400000000,"Symbol":"lpt","Index":168},{"TotalEquity":10715077402,"TotalDebt":0,"BasePrice":2063000000,"Symbol":"lrc","Index":169},{"TotalEquity":8050236298,"TotalDebt":0,"BasePrice":7240000000,"Symbol":"lsk","Index":170},{"TotalEquity":1122426768,"TotalDebt":0,"BasePrice":758900000000,"Symbol":"ltc","Index":171},{"TotalEquity":22654000,"TotalDebt":0,"BasePrice":710000000,"Symbol":"lto","Index":172},{"TotalEquity":16580624988,"TotalDebt":0,"BasePrice":13251000000,"Symbol":"luna","Index":173},{"TotalEquity":1705595428000000,"TotalDebt":0,"BasePrice":1560500,"Symbol":"lunc","Index":174},{"TotalEquity":0,"TotalDebt":0,"BasePrice":4759000000,"Symbol":"magic","Index":175},{"TotalEquity":77632636722,"TotalDebt":0,"BasePrice":3278000000,"Symbol":"mana","Index":176},{"TotalEquity":1990776000,"TotalDebt":0,"BasePrice":23850000000,"Symbol":"mask","Index":177},{"TotalEquity":1076925578756,"TotalDebt":0,"BasePrice":7989000000,"Symbol":"matic","Index":178},{"TotalEquity":2785908800000,"TotalDebt":0,"BasePrice":23690000,"Symbol":"mbl","Index":179},{"TotalEquity":934922304,"TotalDebt":0,"BasePrice":3850000000,"Symbol":"mbox","Index":180},{"TotalEquity":13377446308,"TotalDebt":0,"BasePrice":2670000000,"Symbol":"mc","Index":181},{"TotalEquity":258144000,"TotalDebt":0,"BasePrice":201100000,"Symbol":"mdt","Index":182},{"TotalEquity":3081330908,"TotalDebt":0,"BasePrice":716000000,"Symbol":"mdx","Index":183},{"TotalEquity":32512116000,"TotalDebt":0,"BasePrice":4500000000,"Symbol":"mina","Index":184},{"TotalEquity":12110,"TotalDebt":0,"BasePrice":5400000000000,"Symbol":"mkr","Index":185},{"TotalEquity":0,"TotalDebt":0,"BasePrice":194100000000,"Symbol":"mln","Index":186},{"TotalEquity":132208000000,"TotalDebt":0,"BasePrice":8660000000,"Symbol":"mob","Index":187},{"TotalEquity":262072600,"TotalDebt":0,"BasePrice":63100000000,"Symbol":"movr","Index":188},{"TotalEquity":3096000,"TotalDebt":0,"BasePrice":7020000000,"Symbol":"mtl","Index":189},{"TotalEquity":5615144716,"TotalDebt":0,"BasePrice":15900000000,"Symbol":"near","Index":190},{"TotalEquity":6048000,"TotalDebt":0,"BasePrice":13000000000,"Symbol":"nebl","Index":191},{"TotalEquity":484605847032,"TotalDebt":0,"BasePrice":65600000000,"Symbol":"neo","Index":192},{"TotalEquity":0,"TotalDebt":0,"BasePrice":7260000000,"Symbol":"nexo","Index":193},{"TotalEquity":2013960000,"TotalDebt":0,"BasePrice":862000000,"Symbol":"nkn","Index":194},{"TotalEquity":39400,"TotalDebt":0,"BasePrice":129300000000,"Symbol":"nmr","Index":195},{"TotalEquity":99676000,"TotalDebt":0,"BasePrice":1901000000,"Symbol":"nuls","Index":196},{"TotalEquity":1063446,"TotalDebt":0,"BasePrice":1906000000,"Symbol":"ocean","Index":197},{"TotalEquity":380000,"TotalDebt":0,"BasePrice":23960000000,"Symbol":"og","Index":198},{"TotalEquity":30491752,"TotalDebt":0,"BasePrice":906000000,"Symbol":"ogn","Index":199},{"TotalEquity":117360000,"TotalDebt":0,"BasePrice":289000000,"Symbol":"om","Index":200},{"TotalEquity":213392241236,"TotalDebt":0,"BasePrice":10630000000,"Symbol":"omg","Index":201},{"TotalEquity":561009012134,"TotalDebt":0,"BasePrice":106700000,"Symbol":"one","Index":202},{"TotalEquity":64315053780,"TotalDebt":0,"BasePrice":2177482600,"Symbol":"ong","Index":203},{"TotalEquity":4682530773048,"TotalDebt":0,"BasePrice":1609000000,"Symbol":"ont","Index":204},{"TotalEquity":893960000,"TotalDebt":0,"BasePrice":30800000,"Symbol":"ooki","Index":205},{"TotalEquity":383291200,"TotalDebt":0,"BasePrice":10840000000,"Symbol":"op","Index":206},{"TotalEquity":11568582000,"TotalDebt":0,"BasePrice":7680000000,"Symbol":"orn","Index":207},{"TotalEquity":0,"TotalDebt":0,"BasePrice":7240000000,"Symbol":"osmo","Index":208},{"TotalEquity":178748000,"TotalDebt":0,"BasePrice":687000000,"Symbol":"oxt","Index":209},{"TotalEquity":0,"TotalDebt":0,"BasePrice":18530000000000,"Symbol":"paxg","Index":210},{"TotalEquity":21441646500892,"TotalDebt":0,"BasePrice":215100000,"Symbol":"people","Index":211},{"TotalEquity":1648337620,"TotalDebt":0,"BasePrice":3831300000,"Symbol":"perp","Index":212},{"TotalEquity":0,"TotalDebt":0,"BasePrice":1112000000,"Symbol":"pha","Index":213},{"TotalEquity":35466658000,"TotalDebt":0,"BasePrice":5237000000,"Symbol":"phb","Index":214},{"TotalEquity":28791180000,"TotalDebt":0,"BasePrice":1430000000,"Symbol":"pla","Index":215},{"TotalEquity":175000000,"TotalDebt":0,"BasePrice":1358592400,"Symbol":"pnt","Index":216},{"TotalEquity":3494881620000,"TotalDebt":0,"BasePrice":3570000000,"Symbol":"pols","Index":217},{"TotalEquity":74823148144,"TotalDebt":0,"BasePrice":1234000000,"Symbol":"polyx","Index":218},{"TotalEquity":493224786192,"TotalDebt":0,"BasePrice":77900000,"Symbol":"pond","Index":219},{"TotalEquity":72399098108,"TotalDebt":0,"BasePrice":25696000000,"Symbol":"porto","Index":220},{"TotalEquity":21005000000,"TotalDebt":0,"BasePrice":1273000000,"Symbol":"powr","Index":221},{"TotalEquity":0,"TotalDebt":0,"BasePrice":39200000000,"Symbol":"prom","Index":222},{"TotalEquity":0,"TotalDebt":0,"BasePrice":4230000000,"Symbol":"pros","Index":223},{"TotalEquity":2246200,"TotalDebt":0,"BasePrice":56400000000,"Symbol":"psg","Index":224},{"TotalEquity":57372118540,"TotalDebt":0,"BasePrice":3240000000,"Symbol":"pundix","Index":225},{"TotalEquity":172800,"TotalDebt":0,"BasePrice":29800000000,"Symbol":"pyr","Index":226},{"TotalEquity":152556846850,"TotalDebt":0,"BasePrice":65200000,"Symbol":"qi","Index":227},{"TotalEquity":703867724,"TotalDebt":0,"BasePrice":1118000000000,"Symbol":"qnt","Index":228},{"TotalEquity":209070344,"TotalDebt":0,"BasePrice":19610000000,"Symbol":"qtum","Index":229},{"TotalEquity":107668,"TotalDebt":0,"BasePrice":464000000000,"Symbol":"quick","Index":230},{"TotalEquity":15960000,"TotalDebt":0,"BasePrice":15330000000,"Symbol":"rad","Index":231},{"TotalEquity":0,"TotalDebt":0,"BasePrice":1007000000,"Symbol":"rare","Index":232},{"TotalEquity":20536980000,"TotalDebt":0,"BasePrice":1502000000,"Symbol":"ray","Index":233},{"TotalEquity":2330100436820,"TotalDebt":0,"BasePrice":24230000,"Symbol":"reef","Index":234},{"TotalEquity":692913057840,"TotalDebt":0,"BasePrice":225000000,"Symbol":"rei","Index":235},{"TotalEquity":0,"TotalDebt":0,"BasePrice":630420000,"Symbol":"ren","Index":236},{"TotalEquity":223600190,"TotalDebt":0,"BasePrice":872000000,"Symbol":"req","Index":237},{"TotalEquity":18748000,"TotalDebt":0,"BasePrice":12427749000,"Symbol":"rlc","Index":238},{"TotalEquity":376358800,"TotalDebt":0,"BasePrice":4200000000,"Symbol":"rndr","Index":239},{"TotalEquity":2094224000,"TotalDebt":0,"BasePrice":370400000,"Symbol":"rose","Index":240},{"TotalEquity":119940000,"TotalDebt":0,"BasePrice":31690000,"Symbol":"rsr","Index":241},{"TotalEquity":269393997600,"TotalDebt":0,"BasePrice":13750000000,"Symbol":"rune","Index":242},{"TotalEquity":539117133400,"TotalDebt":0,"BasePrice":203000000,"Symbol":"rvn","Index":243},{"TotalEquity":154754594184,"TotalDebt":0,"BasePrice":4309000000,"Symbol":"sand","Index":244},{"TotalEquity":2790903662,"TotalDebt":0,"BasePrice":44700000000,"Symbol":"santos","Index":245},{"TotalEquity":353200000,"TotalDebt":0,"BasePrice":23600000,"Symbol":"sc","Index":246},{"TotalEquity":0,"TotalDebt":0,"BasePrice":6390000000,"Symbol":"scrt","Index":247},{"TotalEquity":493481218,"TotalDebt":0,"BasePrice":4033000000,"Symbol":"sfp","Index":248},{"TotalEquity":92811810818000000,"TotalDebt":0,"BasePrice":84300,"Symbol":"shib","Index":249},{"TotalEquity":338633610064,"TotalDebt":0,"BasePrice":227300000,"Symbol":"skl","Index":250},{"TotalEquity":17412372632502,"TotalDebt":0,"BasePrice":20900000,"Symbol":"slp","Index":251},{"TotalEquity":19400000,"TotalDebt":0,"BasePrice":4858000000,"Symbol":"snm","Index":252},{"TotalEquity":12518184,"TotalDebt":0,"BasePrice":16280000000,"Symbol":"snx","Index":253},{"TotalEquity":7697220542,"TotalDebt":0,"BasePrice":135100000000,"Symbol":"sol","Index":254},{"TotalEquity":43400244636,"TotalDebt":0,"BasePrice":5522000,"Symbol":"spell","Index":255},{"TotalEquity":145168230000,"TotalDebt":0,"BasePrice":1567800000,"Symbol":"srm","Index":256},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3544000000,"Symbol":"stg","Index":257},{"TotalEquity":1375707000000,"TotalDebt":0,"BasePrice":38110000,"Symbol":"stmx","Index":258},{"TotalEquity":8912432530,"TotalDebt":0,"BasePrice":2582000000,"Symbol":"storj","Index":259},{"TotalEquity":0,"TotalDebt":0,"BasePrice":275900000,"Symbol":"stpt","Index":260},{"TotalEquity":14047500,"TotalDebt":0,"BasePrice":4050000000,"Symbol":"strax","Index":261},{"TotalEquity":1423000,"TotalDebt":0,"BasePrice":2190000000,"Symbol":"stx","Index":262},{"TotalEquity":326978131392,"TotalDebt":0,"BasePrice":50400000,"Symbol":"sun","Index":263},{"TotalEquity":30595425600,"TotalDebt":0,"BasePrice":867000000,"Symbol":"super","Index":264},{"TotalEquity":128556304136,"TotalDebt":0,"BasePrice":10420000000,"Symbol":"sushi","Index":265},{"TotalEquity":1059292108408,"TotalDebt":0,"BasePrice":2130000000,"Symbol":"sxp","Index":266},{"TotalEquity":130320000,"TotalDebt":0,"BasePrice":1017000000,"Symbol":"sys","Index":267},{"TotalEquity":5172000,"TotalDebt":0,"BasePrice":163000000,"Symbol":"t","Index":268},{"TotalEquity":1030910000,"TotalDebt":0,"BasePrice":327000000,"Symbol":"tfuel","Index":269},{"TotalEquity":160460684218,"TotalDebt":0,"BasePrice":7590000000,"Symbol":"theta","Index":270},{"TotalEquity":198770314330,"TotalDebt":0,"BasePrice":2292000000,"Symbol":"tko","Index":271},{"TotalEquity":256387034218,"TotalDebt":0,"BasePrice":128600000,"Symbol":"tlm","Index":272},{"TotalEquity":2508400,"TotalDebt":0,"BasePrice":2762000000,"Symbol":"tomo","Index":273},{"TotalEquity":9400,"TotalDebt":0,"BasePrice":124800000000,"Symbol":"trb","Index":274},{"TotalEquity":33800000,"TotalDebt":0,"BasePrice":2070797400,"Symbol":"tribe","Index":275},{"TotalEquity":46160000,"TotalDebt":0,"BasePrice":25980000,"Symbol":"troy","Index":276},{"TotalEquity":0,"TotalDebt":0,"BasePrice":288071600,"Symbol":"tru","Index":277},{"TotalEquity":2043669562480,"TotalDebt":0,"BasePrice":524600000,"Symbol":"trx","Index":278},{"TotalEquity":63678800000,"TotalDebt":0,"BasePrice":301000000,"Symbol":"tvk","Index":279},{"TotalEquity":0,"TotalDebt":0,"BasePrice":14100000000,"Symbol":"twt","Index":280},{"TotalEquity":13980000,"TotalDebt":0,"BasePrice":15400000000,"Symbol":"uma","Index":281},{"TotalEquity":19120000,"TotalDebt":0,"BasePrice":39360000000,"Symbol":"unfi","Index":282},{"TotalEquity":11981756100,"TotalDebt":0,"BasePrice":55220000000,"Symbol":"uni","Index":283},{"TotalEquity":0,"TotalDebt":0,"BasePrice":10000650400,"Symbol":"usdc","Index":284},{"TotalEquity":12876907115652,"TotalDebt":0,"BasePrice":9997000900,"Symbol":"usdt","Index":285},{"TotalEquity":220063518946,"TotalDebt":0,"BasePrice":203321700,"Symbol":"ustc","Index":286},{"TotalEquity":0,"TotalDebt":0,"BasePrice":777000000,"Symbol":"utk","Index":287},{"TotalEquity":7430929587566,"TotalDebt":0,"BasePrice":164100000,"Symbol":"vet","Index":288},{"TotalEquity":169058297966,"TotalDebt":0,"BasePrice":694900000,"Symbol":"vib","Index":289},{"TotalEquity":252046634,"TotalDebt":0,"BasePrice":195000000,"Symbol":"vite","Index":290},{"TotalEquity":25254109536,"TotalDebt":0,"BasePrice":1671000000,"Symbol":"voxel","Index":291},{"TotalEquity":5153547313742,"TotalDebt":0,"BasePrice":9237200,"Symbol":"vtho","Index":292},{"TotalEquity":17493828000,"TotalDebt":0,"BasePrice":1658321600,"Symbol":"wan","Index":293},{"TotalEquity":2852616,"TotalDebt":0,"BasePrice":14130000000,"Symbol":"waves","Index":294},{"TotalEquity":20000180,"TotalDebt":0,"BasePrice":440000000,"Symbol":"waxp","Index":295},{"TotalEquity":24776160000000,"TotalDebt":0,"BasePrice":738000,"Symbol":"win","Index":296},{"TotalEquity":2370200,"TotalDebt":0,"BasePrice":52100000000,"Symbol":"wing","Index":297},{"TotalEquity":0,"TotalDebt":0,"BasePrice":80975707300,"Symbol":"wnxm","Index":298},{"TotalEquity":75262779600,"TotalDebt":0,"BasePrice":1347000000,"Symbol":"woo","Index":299},{"TotalEquity":415631596070,"TotalDebt":0,"BasePrice":1401000000,"Symbol":"wrx","Index":300},{"TotalEquity":183890000,"TotalDebt":0,"BasePrice":1916523600,"Symbol":"wtc","Index":301},{"TotalEquity":172906064000000,"TotalDebt":0,"BasePrice":246700,"Symbol":"xec","Index":302},{"TotalEquity":129072400,"TotalDebt":0,"BasePrice":291912400,"Symbol":"xem","Index":303},{"TotalEquity":152986398800,"TotalDebt":0,"BasePrice":751000000,"Symbol":"xlm","Index":304},{"TotalEquity":109317164,"TotalDebt":0,"BasePrice":1548000000000,"Symbol":"xmr","Index":305},{"TotalEquity":1954309930640,"TotalDebt":0,"BasePrice":3442000000,"Symbol":"xrp","Index":306},{"TotalEquity":388360923948,"TotalDebt":0,"BasePrice":7720000000,"Symbol":"xtz","Index":307},{"TotalEquity":45916405132400,"TotalDebt":0,"BasePrice":27200000,"Symbol":"xvg","Index":308},{"TotalEquity":1725600,"TotalDebt":0,"BasePrice":42900000000,"Symbol":"xvs","Index":309},{"TotalEquity":1940,"TotalDebt":0,"BasePrice":54420000000000,"Symbol":"yfi","Index":310},{"TotalEquity":393918000,"TotalDebt":0,"BasePrice":1749000000,"Symbol":"ygg","Index":311},{"TotalEquity":4124782260,"TotalDebt":0,"BasePrice":414000000000,"Symbol":"zec","Index":312},{"TotalEquity":1900092,"TotalDebt":0,"BasePrice":84900000000,"Symbol":"zen","Index":313},{"TotalEquity":2075635646560,"TotalDebt":0,"BasePrice":174100000,"Symbol":"zil","Index":314},{"TotalEquity":119194400,"TotalDebt":0,"BasePrice":1603000000,"Symbol":"zrx","Index":315}]
```

Each time after generating proof data, you need to query cex assets once, and then save this data, which will be used in the `CexAssetsInfo` field of the following `cex_config.json`.

> Note: The proof.csv file here should be from the same batch as the saved asset proof data, otherwise the verification may fail.

#### Configuration File

cex_config.json is the configuration file for verifying the exchange assets.

```Plaintext
{
  "ProofCsv": "./config/proof.csv",
  "ZkKeyVKDirectoryAndPrefix": "./zkpor864",
  "CexAssetsInfo": [{"TotalEquity":10049232946,"TotalDebt":0,"BasePrice":3960000000,"Symbol":"1inch","Index":0},{"TotalEquity":421836,"TotalDebt":0,"BasePrice":564000000000,"Symbol":"aave","Index":1},{"TotalEquity":0,"TotalDebt":0,"BasePrice":79800000,"Symbol":"ach","Index":2},{"TotalEquity":3040000,"TotalDebt":0,"BasePrice":25460000000,"Symbol":"acm","Index":3},{"TotalEquity":17700050162640,"TotalDebt":0,"BasePrice":2784000000,"Symbol":"ada","Index":4},{"TotalEquity":485400000,"TotalDebt":0,"BasePrice":1182000000,"Symbol":"adx","Index":5},{"TotalEquity":0,"TotalDebt":0,"BasePrice":907000000,"Symbol":"aergo","Index":6},{"TotalEquity":0,"TotalDebt":0,"BasePrice":2720000000,"Symbol":"agld","Index":7},{"TotalEquity":1969000000,"TotalDebt":0,"BasePrice":30500000,"Symbol":"akro","Index":8},{"TotalEquity":0,"TotalDebt":0,"BasePrice":141000000000,"Symbol":"alcx","Index":9},{"TotalEquity":15483340912,"TotalDebt":0,"BasePrice":1890000000,"Symbol":"algo","Index":10},{"TotalEquity":3187400,"TotalDebt":0,"BasePrice":11350000000,"Symbol":"alice","Index":11},{"TotalEquity":1760000,"TotalDebt":0,"BasePrice":2496000000,"Symbol":"alpaca","Index":12},{"TotalEquity":84596857600,"TotalDebt":0,"BasePrice":785000000,"Symbol":"alpha","Index":13},{"TotalEquity":3672090936,"TotalDebt":0,"BasePrice":20849000000,"Symbol":"alpine","Index":14},{"TotalEquity":198200000,"TotalDebt":0,"BasePrice":132600000,"Symbol":"amb","Index":15},{"TotalEquity":53800000,"TotalDebt":0,"BasePrice":32200000,"Symbol":"amp","Index":16},{"TotalEquity":3291606210,"TotalDebt":0,"BasePrice":340300000,"Symbol":"anc","Index":17},{"TotalEquity":192954000,"TotalDebt":0,"BasePrice":166000000,"Symbol":"ankr","Index":18},{"TotalEquity":2160000,"TotalDebt":0,"BasePrice":20940000000,"Symbol":"ant","Index":19},{"TotalEquity":5995002000,"TotalDebt":0,"BasePrice":40370000000,"Symbol":"ape","Index":20},{"TotalEquity":0,"TotalDebt":0,"BasePrice":11110000000,"Symbol":"api3","Index":21},{"TotalEquity":53728000,"TotalDebt":0,"BasePrice":38560000000,"Symbol":"apt","Index":22},{"TotalEquity":0,"TotalDebt":0,"BasePrice":68500000000,"Symbol":"ar","Index":23},{"TotalEquity":55400000,"TotalDebt":0,"BasePrice":667648400,"Symbol":"ardr","Index":24},{"TotalEquity":8320000,"TotalDebt":0,"BasePrice":266200000,"Symbol":"arpa","Index":25},{"TotalEquity":18820000,"TotalDebt":0,"BasePrice":401000000,"Symbol":"astr","Index":26},{"TotalEquity":13205405410,"TotalDebt":0,"BasePrice":934000000,"Symbol":"ata","Index":27},{"TotalEquity":7016230960,"TotalDebt":0,"BasePrice":102450000000,"Symbol":"atom","Index":28},{"TotalEquity":2619441828,"TotalDebt":0,"BasePrice":40900000000,"Symbol":"auction","Index":29},{"TotalEquity":9640198,"TotalDebt":0,"BasePrice":1432000000,"Symbol":"audio","Index":30},{"TotalEquity":0,"TotalDebt":0,"BasePrice":2306000000000,"Symbol":"auto","Index":31},{"TotalEquity":886400,"TotalDebt":0,"BasePrice":5390000000,"Symbol":"ava","Index":32},{"TotalEquity":2883562350,"TotalDebt":0,"BasePrice":117800000000,"Symbol":"avax","Index":33},{"TotalEquity":1864300912,"TotalDebt":0,"BasePrice":68200000000,"Symbol":"axs","Index":34},{"TotalEquity":843870,"TotalDebt":0,"BasePrice":23700000000,"Symbol":"badger","Index":35},{"TotalEquity":114869291528,"TotalDebt":0,"BasePrice":1379000000,"Symbol":"bake","Index":36},{"TotalEquity":95400,"TotalDebt":0,"BasePrice":54110000000,"Symbol":"bal","Index":37},{"TotalEquity":123113880,"TotalDebt":0,"BasePrice":14610000000,"Symbol":"band","Index":38},{"TotalEquity":0,"TotalDebt":0,"BasePrice":37100000000,"Symbol":"bar","Index":39},{"TotalEquity":73090049578,"TotalDebt":0,"BasePrice":1774000000,"Symbol":"bat","Index":40},{"TotalEquity":28891300,"TotalDebt":0,"BasePrice":1017000000000,"Symbol":"bch","Index":41},{"TotalEquity":19889623294,"TotalDebt":0,"BasePrice":4130000000,"Symbol":"bel","Index":42},{"TotalEquity":374840602180,"TotalDebt":0,"BasePrice":699700000,"Symbol":"beta","Index":43},{"TotalEquity":270294580,"TotalDebt":0,"BasePrice":12290900000000,"Symbol":"beth","Index":44},{"TotalEquity":35692901600,"TotalDebt":0,"BasePrice":2730000000,"Symbol":"bico","Index":45},{"TotalEquity":0,"TotalDebt":0,"BasePrice":639000,"Symbol":"bidr","Index":46},{"TotalEquity":240200000,"TotalDebt":0,"BasePrice":538000000,"Symbol":"blz","Index":47},{"TotalEquity":83614634622,"TotalDebt":0,"BasePrice":2599000000000,"Symbol":"bnb","Index":48},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3490000000,"Symbol":"bnt","Index":49},{"TotalEquity":1560,"TotalDebt":0,"BasePrice":592000000000,"Symbol":"bnx","Index":50},{"TotalEquity":2076000,"TotalDebt":0,"BasePrice":32630000000,"Symbol":"bond","Index":51},{"TotalEquity":44699589660,"TotalDebt":0,"BasePrice":1768000000,"Symbol":"bsw","Index":52},{"TotalEquity":291716078,"TotalDebt":0,"BasePrice":169453900000000,"Symbol":"btc","Index":53},{"TotalEquity":15500321300000000,"TotalDebt":0,"BasePrice":6300,"Symbol":"bttc","Index":54},{"TotalEquity":70771546756,"TotalDebt":0,"BasePrice":5240000000,"Symbol":"burger","Index":55},{"TotalEquity":12058907297354,"TotalDebt":1476223055432,"BasePrice":10000000000,"Symbol":"busd","Index":56},{"TotalEquity":34716440000,"TotalDebt":0,"BasePrice":1647000000,"Symbol":"c98","Index":57},{"TotalEquity":1541723702,"TotalDebt":0,"BasePrice":33140000000,"Symbol":"cake","Index":58},{"TotalEquity":2112000,"TotalDebt":0,"BasePrice":5200000000,"Symbol":"celo","Index":59},{"TotalEquity":317091540000,"TotalDebt":0,"BasePrice":101000000,"Symbol":"celr","Index":60},{"TotalEquity":137111365560,"TotalDebt":0,"BasePrice":228000000,"Symbol":"cfx","Index":61},{"TotalEquity":0,"TotalDebt":0,"BasePrice":1820000000,"Symbol":"chess","Index":62},{"TotalEquity":258540000,"TotalDebt":0,"BasePrice":1140000000,"Symbol":"chr","Index":63},{"TotalEquity":289172288882,"TotalDebt":0,"BasePrice":1099000000,"Symbol":"chz","Index":64},{"TotalEquity":0,"TotalDebt":0,"BasePrice":25100000,"Symbol":"ckb","Index":65},{"TotalEquity":1851135024806,"TotalDebt":0,"BasePrice":535500000,"Symbol":"clv","Index":66},{"TotalEquity":155010000,"TotalDebt":0,"BasePrice":5202000000,"Symbol":"cocos","Index":67},{"TotalEquity":52093390,"TotalDebt":0,"BasePrice":335800000000,"Symbol":"comp","Index":68},{"TotalEquity":13991592000,"TotalDebt":0,"BasePrice":44500000,"Symbol":"cos","Index":69},{"TotalEquity":51240788068,"TotalDebt":0,"BasePrice":557000000,"Symbol":"coti","Index":70},{"TotalEquity":0,"TotalDebt":0,"BasePrice":107900000000,"Symbol":"cream","Index":71},{"TotalEquity":15940224,"TotalDebt":0,"BasePrice":5470000000,"Symbol":"crv","Index":72},{"TotalEquity":2336000,"TotalDebt":0,"BasePrice":7450000000,"Symbol":"ctk","Index":73},{"TotalEquity":88860000,"TotalDebt":0,"BasePrice":1059000000,"Symbol":"ctsi","Index":74},{"TotalEquity":440400000,"TotalDebt":0,"BasePrice":1763000000,"Symbol":"ctxc","Index":75},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3375000000,"Symbol":"cvp","Index":76},{"TotalEquity":176202,"TotalDebt":0,"BasePrice":30810000000,"Symbol":"cvx","Index":77},{"TotalEquity":0,"TotalDebt":0,"BasePrice":9999000100,"Symbol":"dai","Index":78},{"TotalEquity":90702266836,"TotalDebt":0,"BasePrice":1293500000,"Symbol":"dar","Index":79},{"TotalEquity":29386961406,"TotalDebt":0,"BasePrice":458300000000,"Symbol":"dash","Index":80},{"TotalEquity":1628888000,"TotalDebt":0,"BasePrice":235500000,"Symbol":"data","Index":81},{"TotalEquity":0,"TotalDebt":0,"BasePrice":186229836100,"Symbol":"dcr","Index":82},{"TotalEquity":0,"TotalDebt":0,"BasePrice":15920000000,"Symbol":"dego","Index":83},{"TotalEquity":26105549312822,"TotalDebt":0,"BasePrice":6830000,"Symbol":"dent","Index":84},{"TotalEquity":670658000,"TotalDebt":0,"BasePrice":24000000000,"Symbol":"dexe","Index":85},{"TotalEquity":517372774000,"TotalDebt":0,"BasePrice":82200000,"Symbol":"dgb","Index":86},{"TotalEquity":1120000,"TotalDebt":0,"BasePrice":2970000000,"Symbol":"dia","Index":87},{"TotalEquity":0,"TotalDebt":0,"BasePrice":151800000,"Symbol":"dock","Index":88},{"TotalEquity":19453393384,"TotalDebt":0,"BasePrice":987000000,"Symbol":"dodo","Index":89},{"TotalEquity":25526548451614,"TotalDebt":0,"BasePrice":723900000,"Symbol":"doge","Index":90},{"TotalEquity":466049240950,"TotalDebt":0,"BasePrice":46820000000,"Symbol":"dot","Index":91},{"TotalEquity":69200000,"TotalDebt":0,"BasePrice":3138000000,"Symbol":"drep","Index":92},{"TotalEquity":0,"TotalDebt":0,"BasePrice":870000000,"Symbol":"dusk","Index":93},{"TotalEquity":45675816000,"TotalDebt":0,"BasePrice":12120000000,"Symbol":"dydx","Index":94},{"TotalEquity":241920370,"TotalDebt":0,"BasePrice":343400000000,"Symbol":"egld","Index":95},{"TotalEquity":3640000,"TotalDebt":0,"BasePrice":1691000000,"Symbol":"elf","Index":96},{"TotalEquity":200008070,"TotalDebt":0,"BasePrice":2556000000,"Symbol":"enj","Index":97},{"TotalEquity":836000,"TotalDebt":0,"BasePrice":115500000000,"Symbol":"ens","Index":98},{"TotalEquity":23489390223668,"TotalDebt":0,"BasePrice":8960000000,"Symbol":"eos","Index":99},{"TotalEquity":83358943947200,"TotalDebt":0,"BasePrice":2960000,"Symbol":"epx","Index":100},{"TotalEquity":1539180000,"TotalDebt":0,"BasePrice":17540000000,"Symbol":"ern","Index":101},{"TotalEquity":48056621250,"TotalDebt":0,"BasePrice":204100000000,"Symbol":"etc","Index":102},{"TotalEquity":28478224392,"TotalDebt":0,"BasePrice":12688000000000,"Symbol":"eth","Index":103},{"TotalEquity":21790805772,"TotalDebt":0,"BasePrice":10641000000,"Symbol":"eur","Index":104},{"TotalEquity":196200,"TotalDebt":0,"BasePrice":307000000000,"Symbol":"farm","Index":105},{"TotalEquity":31040000,"TotalDebt":0,"BasePrice":1240000000,"Symbol":"fet","Index":106},{"TotalEquity":26460000,"TotalDebt":0,"BasePrice":3354000000,"Symbol":"fida","Index":107},{"TotalEquity":5539231876,"TotalDebt":0,"BasePrice":33380000000,"Symbol":"fil","Index":108},{"TotalEquity":152000000,"TotalDebt":0,"BasePrice":275000000,"Symbol":"fio","Index":109},{"TotalEquity":1014252612,"TotalDebt":0,"BasePrice":16540000000,"Symbol":"firo","Index":110},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3313000000,"Symbol":"fis","Index":111},{"TotalEquity":0,"TotalDebt":0,"BasePrice":765931600,"Symbol":"flm","Index":112},{"TotalEquity":3688000,"TotalDebt":0,"BasePrice":6990000000,"Symbol":"flow","Index":113},{"TotalEquity":0,"TotalDebt":0,"BasePrice":5090000000,"Symbol":"flux","Index":114},{"TotalEquity":0,"TotalDebt":0,"BasePrice":162500000,"Symbol":"for","Index":115},{"TotalEquity":80000,"TotalDebt":0,"BasePrice":29400000000,"Symbol":"forth","Index":116},{"TotalEquity":14430200000,"TotalDebt":0,"BasePrice":1808000000,"Symbol":"front","Index":117},{"TotalEquity":26629480000,"TotalDebt":0,"BasePrice":2211000000,"Symbol":"ftm","Index":118},{"TotalEquity":16207428000,"TotalDebt":0,"BasePrice":9125000000,"Symbol":"ftt","Index":119},{"TotalEquity":679597613272,"TotalDebt":0,"BasePrice":61663700,"Symbol":"fun","Index":120},{"TotalEquity":0,"TotalDebt":0,"BasePrice":51410000000,"Symbol":"fxs","Index":121},{"TotalEquity":4110633550,"TotalDebt":0,"BasePrice":11540000000,"Symbol":"gal","Index":122},{"TotalEquity":2551466375170,"TotalDebt":0,"BasePrice":234700000,"Symbol":"gala","Index":123},{"TotalEquity":1252940134,"TotalDebt":0,"BasePrice":20260000000,"Symbol":"gas","Index":124},{"TotalEquity":0,"TotalDebt":0,"BasePrice":1850000000,"Symbol":"glm","Index":125},{"TotalEquity":25058958996,"TotalDebt":0,"BasePrice":3195000000,"Symbol":"glmr","Index":126},{"TotalEquity":443980786672,"TotalDebt":0,"BasePrice":2588000000,"Symbol":"gmt","Index":127},{"TotalEquity":160000,"TotalDebt":0,"BasePrice":417300000000,"Symbol":"gmx","Index":128},{"TotalEquity":178800,"TotalDebt":0,"BasePrice":878736379100,"Symbol":"gno","Index":129},{"TotalEquity":6828000,"TotalDebt":0,"BasePrice":620000000,"Symbol":"grt","Index":130},{"TotalEquity":20784000,"TotalDebt":0,"BasePrice":13340000000,"Symbol":"gtc","Index":131},{"TotalEquity":94280000,"TotalDebt":0,"BasePrice":1494000000,"Symbol":"hard","Index":132},{"TotalEquity":336206273140,"TotalDebt":0,"BasePrice":391000000,"Symbol":"hbar","Index":133},{"TotalEquity":1791317190,"TotalDebt":0,"BasePrice":8870000000,"Symbol":"high","Index":134},{"TotalEquity":6485637600,"TotalDebt":0,"BasePrice":2700000000,"Symbol":"hive","Index":135},{"TotalEquity":1956144,"TotalDebt":0,"BasePrice":18400000000,"Symbol":"hnt","Index":136},{"TotalEquity":9587039140000,"TotalDebt":0,"BasePrice":14820000,"Symbol":"hot","Index":137},{"TotalEquity":223895102366,"TotalDebt":0,"BasePrice":38980000000,"Symbol":"icp","Index":138},{"TotalEquity":52168047570,"TotalDebt":0,"BasePrice":1516000000,"Symbol":"icx","Index":139},{"TotalEquity":15480000,"TotalDebt":0,"BasePrice":388000000,"Symbol":"idex","Index":140},{"TotalEquity":8400000,"TotalDebt":0,"BasePrice":388700000000,"Symbol":"ilv","Index":141},{"TotalEquity":12686368000,"TotalDebt":0,"BasePrice":4230000000,"Symbol":"imx","Index":142},{"TotalEquity":139990936000,"TotalDebt":0,"BasePrice":13680000000,"Symbol":"inj","Index":143},{"TotalEquity":69430091021436,"TotalDebt":0,"BasePrice":72500000,"Symbol":"iost","Index":144},{"TotalEquity":71259628200,"TotalDebt":0,"BasePrice":1823000000,"Symbol":"iota","Index":145},{"TotalEquity":428000000,"TotalDebt":0,"BasePrice":221500000,"Symbol":"iotx","Index":146},{"TotalEquity":858126200,"TotalDebt":0,"BasePrice":43200000,"Symbol":"iq","Index":147},{"TotalEquity":8680000,"TotalDebt":0,"BasePrice":132174000,"Symbol":"iris","Index":148},{"TotalEquity":1889177748140,"TotalDebt":0,"BasePrice":37600000,"Symbol":"jasmy","Index":149},{"TotalEquity":2000,"TotalDebt":0,"BasePrice":1416000000,"Symbol":"joe","Index":150},{"TotalEquity":927921956,"TotalDebt":0,"BasePrice":201400000,"Symbol":"jst","Index":151},{"TotalEquity":560000,"TotalDebt":0,"BasePrice":6590000000,"Symbol":"kava","Index":152},{"TotalEquity":30527442000,"TotalDebt":0,"BasePrice":9480000000,"Symbol":"kda","Index":153},{"TotalEquity":7587760000,"TotalDebt":0,"BasePrice":29350000,"Symbol":"key","Index":154},{"TotalEquity":372181704,"TotalDebt":0,"BasePrice":1613000000,"Symbol":"klay","Index":155},{"TotalEquity":81600000,"TotalDebt":0,"BasePrice":1904661800,"Symbol":"kmd","Index":156},{"TotalEquity":493317080,"TotalDebt":0,"BasePrice":4940000000,"Symbol":"knc","Index":157},{"TotalEquity":1700000,"TotalDebt":0,"BasePrice":621600000000,"Symbol":"kp3r","Index":158},{"TotalEquity":27180,"TotalDebt":0,"BasePrice":250100000000,"Symbol":"ksm","Index":159},{"TotalEquity":1656679204,"TotalDebt":0,"BasePrice":30978000000,"Symbol":"lazio","Index":160},{"TotalEquity":295510852208,"TotalDebt":0,"BasePrice":15200000000,"Symbol":"ldo","Index":161},{"TotalEquity":1158728143570,"TotalDebt":0,"BasePrice":17230000,"Symbol":"lever","Index":162},{"TotalEquity":6505365672842,"TotalDebt":0,"BasePrice":52690000,"Symbol":"lina","Index":163},{"TotalEquity":8162369516,"TotalDebt":0,"BasePrice":57120000000,"Symbol":"link","Index":164},{"TotalEquity":95484000,"TotalDebt":0,"BasePrice":7220000000,"Symbol":"lit","Index":165},{"TotalEquity":12682220,"TotalDebt":0,"BasePrice":3632000000,"Symbol":"loka","Index":166},{"TotalEquity":0,"TotalDebt":0,"BasePrice":409400000,"Symbol":"loom","Index":167},{"TotalEquity":0,"TotalDebt":0,"BasePrice":44400000000,"Symbol":"lpt","Index":168},{"TotalEquity":10715077402,"TotalDebt":0,"BasePrice":2063000000,"Symbol":"lrc","Index":169},{"TotalEquity":8050236298,"TotalDebt":0,"BasePrice":7240000000,"Symbol":"lsk","Index":170},{"TotalEquity":1122426768,"TotalDebt":0,"BasePrice":758900000000,"Symbol":"ltc","Index":171},{"TotalEquity":22654000,"TotalDebt":0,"BasePrice":710000000,"Symbol":"lto","Index":172},{"TotalEquity":16580624988,"TotalDebt":0,"BasePrice":13251000000,"Symbol":"luna","Index":173},{"TotalEquity":1705595428000000,"TotalDebt":0,"BasePrice":1560500,"Symbol":"lunc","Index":174},{"TotalEquity":0,"TotalDebt":0,"BasePrice":4759000000,"Symbol":"magic","Index":175},{"TotalEquity":77632636722,"TotalDebt":0,"BasePrice":3278000000,"Symbol":"mana","Index":176},{"TotalEquity":1990776000,"TotalDebt":0,"BasePrice":23850000000,"Symbol":"mask","Index":177},{"TotalEquity":1076925578756,"TotalDebt":0,"BasePrice":7989000000,"Symbol":"matic","Index":178},{"TotalEquity":2785908800000,"TotalDebt":0,"BasePrice":23690000,"Symbol":"mbl","Index":179},{"TotalEquity":934922304,"TotalDebt":0,"BasePrice":3850000000,"Symbol":"mbox","Index":180},{"TotalEquity":13377446308,"TotalDebt":0,"BasePrice":2670000000,"Symbol":"mc","Index":181},{"TotalEquity":258144000,"TotalDebt":0,"BasePrice":201100000,"Symbol":"mdt","Index":182},{"TotalEquity":3081330908,"TotalDebt":0,"BasePrice":716000000,"Symbol":"mdx","Index":183},{"TotalEquity":32512116000,"TotalDebt":0,"BasePrice":4500000000,"Symbol":"mina","Index":184},{"TotalEquity":12110,"TotalDebt":0,"BasePrice":5400000000000,"Symbol":"mkr","Index":185},{"TotalEquity":0,"TotalDebt":0,"BasePrice":194100000000,"Symbol":"mln","Index":186},{"TotalEquity":132208000000,"TotalDebt":0,"BasePrice":8660000000,"Symbol":"mob","Index":187},{"TotalEquity":262072600,"TotalDebt":0,"BasePrice":63100000000,"Symbol":"movr","Index":188},{"TotalEquity":3096000,"TotalDebt":0,"BasePrice":7020000000,"Symbol":"mtl","Index":189},{"TotalEquity":5615144716,"TotalDebt":0,"BasePrice":15900000000,"Symbol":"near","Index":190},{"TotalEquity":6048000,"TotalDebt":0,"BasePrice":13000000000,"Symbol":"nebl","Index":191},{"TotalEquity":484605847032,"TotalDebt":0,"BasePrice":65600000000,"Symbol":"neo","Index":192},{"TotalEquity":0,"TotalDebt":0,"BasePrice":7260000000,"Symbol":"nexo","Index":193},{"TotalEquity":2013960000,"TotalDebt":0,"BasePrice":862000000,"Symbol":"nkn","Index":194},{"TotalEquity":39400,"TotalDebt":0,"BasePrice":129300000000,"Symbol":"nmr","Index":195},{"TotalEquity":99676000,"TotalDebt":0,"BasePrice":1901000000,"Symbol":"nuls","Index":196},{"TotalEquity":1063446,"TotalDebt":0,"BasePrice":1906000000,"Symbol":"ocean","Index":197},{"TotalEquity":380000,"TotalDebt":0,"BasePrice":23960000000,"Symbol":"og","Index":198},{"TotalEquity":30491752,"TotalDebt":0,"BasePrice":906000000,"Symbol":"ogn","Index":199},{"TotalEquity":117360000,"TotalDebt":0,"BasePrice":289000000,"Symbol":"om","Index":200},{"TotalEquity":213392241236,"TotalDebt":0,"BasePrice":10630000000,"Symbol":"omg","Index":201},{"TotalEquity":561009012134,"TotalDebt":0,"BasePrice":106700000,"Symbol":"one","Index":202},{"TotalEquity":64315053780,"TotalDebt":0,"BasePrice":2177482600,"Symbol":"ong","Index":203},{"TotalEquity":4682530773048,"TotalDebt":0,"BasePrice":1609000000,"Symbol":"ont","Index":204},{"TotalEquity":893960000,"TotalDebt":0,"BasePrice":30800000,"Symbol":"ooki","Index":205},{"TotalEquity":383291200,"TotalDebt":0,"BasePrice":10840000000,"Symbol":"op","Index":206},{"TotalEquity":11568582000,"TotalDebt":0,"BasePrice":7680000000,"Symbol":"orn","Index":207},{"TotalEquity":0,"TotalDebt":0,"BasePrice":7240000000,"Symbol":"osmo","Index":208},{"TotalEquity":178748000,"TotalDebt":0,"BasePrice":687000000,"Symbol":"oxt","Index":209},{"TotalEquity":0,"TotalDebt":0,"BasePrice":18530000000000,"Symbol":"paxg","Index":210},{"TotalEquity":21441646500892,"TotalDebt":0,"BasePrice":215100000,"Symbol":"people","Index":211},{"TotalEquity":1648337620,"TotalDebt":0,"BasePrice":3831300000,"Symbol":"perp","Index":212},{"TotalEquity":0,"TotalDebt":0,"BasePrice":1112000000,"Symbol":"pha","Index":213},{"TotalEquity":35466658000,"TotalDebt":0,"BasePrice":5237000000,"Symbol":"phb","Index":214},{"TotalEquity":28791180000,"TotalDebt":0,"BasePrice":1430000000,"Symbol":"pla","Index":215},{"TotalEquity":175000000,"TotalDebt":0,"BasePrice":1358592400,"Symbol":"pnt","Index":216},{"TotalEquity":3494881620000,"TotalDebt":0,"BasePrice":3570000000,"Symbol":"pols","Index":217},{"TotalEquity":74823148144,"TotalDebt":0,"BasePrice":1234000000,"Symbol":"polyx","Index":218},{"TotalEquity":493224786192,"TotalDebt":0,"BasePrice":77900000,"Symbol":"pond","Index":219},{"TotalEquity":72399098108,"TotalDebt":0,"BasePrice":25696000000,"Symbol":"porto","Index":220},{"TotalEquity":21005000000,"TotalDebt":0,"BasePrice":1273000000,"Symbol":"powr","Index":221},{"TotalEquity":0,"TotalDebt":0,"BasePrice":39200000000,"Symbol":"prom","Index":222},{"TotalEquity":0,"TotalDebt":0,"BasePrice":4230000000,"Symbol":"pros","Index":223},{"TotalEquity":2246200,"TotalDebt":0,"BasePrice":56400000000,"Symbol":"psg","Index":224},{"TotalEquity":57372118540,"TotalDebt":0,"BasePrice":3240000000,"Symbol":"pundix","Index":225},{"TotalEquity":172800,"TotalDebt":0,"BasePrice":29800000000,"Symbol":"pyr","Index":226},{"TotalEquity":152556846850,"TotalDebt":0,"BasePrice":65200000,"Symbol":"qi","Index":227},{"TotalEquity":703867724,"TotalDebt":0,"BasePrice":1118000000000,"Symbol":"qnt","Index":228},{"TotalEquity":209070344,"TotalDebt":0,"BasePrice":19610000000,"Symbol":"qtum","Index":229},{"TotalEquity":107668,"TotalDebt":0,"BasePrice":464000000000,"Symbol":"quick","Index":230},{"TotalEquity":15960000,"TotalDebt":0,"BasePrice":15330000000,"Symbol":"rad","Index":231},{"TotalEquity":0,"TotalDebt":0,"BasePrice":1007000000,"Symbol":"rare","Index":232},{"TotalEquity":20536980000,"TotalDebt":0,"BasePrice":1502000000,"Symbol":"ray","Index":233},{"TotalEquity":2330100436820,"TotalDebt":0,"BasePrice":24230000,"Symbol":"reef","Index":234},{"TotalEquity":692913057840,"TotalDebt":0,"BasePrice":225000000,"Symbol":"rei","Index":235},{"TotalEquity":0,"TotalDebt":0,"BasePrice":630420000,"Symbol":"ren","Index":236},{"TotalEquity":223600190,"TotalDebt":0,"BasePrice":872000000,"Symbol":"req","Index":237},{"TotalEquity":18748000,"TotalDebt":0,"BasePrice":12427749000,"Symbol":"rlc","Index":238},{"TotalEquity":376358800,"TotalDebt":0,"BasePrice":4200000000,"Symbol":"rndr","Index":239},{"TotalEquity":2094224000,"TotalDebt":0,"BasePrice":370400000,"Symbol":"rose","Index":240},{"TotalEquity":119940000,"TotalDebt":0,"BasePrice":31690000,"Symbol":"rsr","Index":241},{"TotalEquity":269393997600,"TotalDebt":0,"BasePrice":13750000000,"Symbol":"rune","Index":242},{"TotalEquity":539117133400,"TotalDebt":0,"BasePrice":203000000,"Symbol":"rvn","Index":243},{"TotalEquity":154754594184,"TotalDebt":0,"BasePrice":4309000000,"Symbol":"sand","Index":244},{"TotalEquity":2790903662,"TotalDebt":0,"BasePrice":44700000000,"Symbol":"santos","Index":245},{"TotalEquity":353200000,"TotalDebt":0,"BasePrice":23600000,"Symbol":"sc","Index":246},{"TotalEquity":0,"TotalDebt":0,"BasePrice":6390000000,"Symbol":"scrt","Index":247},{"TotalEquity":493481218,"TotalDebt":0,"BasePrice":4033000000,"Symbol":"sfp","Index":248},{"TotalEquity":92811810818000000,"TotalDebt":0,"BasePrice":84300,"Symbol":"shib","Index":249},{"TotalEquity":338633610064,"TotalDebt":0,"BasePrice":227300000,"Symbol":"skl","Index":250},{"TotalEquity":17412372632502,"TotalDebt":0,"BasePrice":20900000,"Symbol":"slp","Index":251},{"TotalEquity":19400000,"TotalDebt":0,"BasePrice":4858000000,"Symbol":"snm","Index":252},{"TotalEquity":12518184,"TotalDebt":0,"BasePrice":16280000000,"Symbol":"snx","Index":253},{"TotalEquity":7697220542,"TotalDebt":0,"BasePrice":135100000000,"Symbol":"sol","Index":254},{"TotalEquity":43400244636,"TotalDebt":0,"BasePrice":5522000,"Symbol":"spell","Index":255},{"TotalEquity":145168230000,"TotalDebt":0,"BasePrice":1567800000,"Symbol":"srm","Index":256},{"TotalEquity":0,"TotalDebt":0,"BasePrice":3544000000,"Symbol":"stg","Index":257},{"TotalEquity":1375707000000,"TotalDebt":0,"BasePrice":38110000,"Symbol":"stmx","Index":258},{"TotalEquity":8912432530,"TotalDebt":0,"BasePrice":2582000000,"Symbol":"storj","Index":259},{"TotalEquity":0,"TotalDebt":0,"BasePrice":275900000,"Symbol":"stpt","Index":260},{"TotalEquity":14047500,"TotalDebt":0,"BasePrice":4050000000,"Symbol":"strax","Index":261},{"TotalEquity":1423000,"TotalDebt":0,"BasePrice":2190000000,"Symbol":"stx","Index":262},{"TotalEquity":326978131392,"TotalDebt":0,"BasePrice":50400000,"Symbol":"sun","Index":263},{"TotalEquity":30595425600,"TotalDebt":0,"BasePrice":867000000,"Symbol":"super","Index":264},{"TotalEquity":128556304136,"TotalDebt":0,"BasePrice":10420000000,"Symbol":"sushi","Index":265},{"TotalEquity":1059292108408,"TotalDebt":0,"BasePrice":2130000000,"Symbol":"sxp","Index":266},{"TotalEquity":130320000,"TotalDebt":0,"BasePrice":1017000000,"Symbol":"sys","Index":267},{"TotalEquity":5172000,"TotalDebt":0,"BasePrice":163000000,"Symbol":"t","Index":268},{"TotalEquity":1030910000,"TotalDebt":0,"BasePrice":327000000,"Symbol":"tfuel","Index":269},{"TotalEquity":160460684218,"TotalDebt":0,"BasePrice":7590000000,"Symbol":"theta","Index":270},{"TotalEquity":198770314330,"TotalDebt":0,"BasePrice":2292000000,"Symbol":"tko","Index":271},{"TotalEquity":256387034218,"TotalDebt":0,"BasePrice":128600000,"Symbol":"tlm","Index":272},{"TotalEquity":2508400,"TotalDebt":0,"BasePrice":2762000000,"Symbol":"tomo","Index":273},{"TotalEquity":9400,"TotalDebt":0,"BasePrice":124800000000,"Symbol":"trb","Index":274},{"TotalEquity":33800000,"TotalDebt":0,"BasePrice":2070797400,"Symbol":"tribe","Index":275},{"TotalEquity":46160000,"TotalDebt":0,"BasePrice":25980000,"Symbol":"troy","Index":276},{"TotalEquity":0,"TotalDebt":0,"BasePrice":288071600,"Symbol":"tru","Index":277},{"TotalEquity":2043669562480,"TotalDebt":0,"BasePrice":524600000,"Symbol":"trx","Index":278},{"TotalEquity":63678800000,"TotalDebt":0,"BasePrice":301000000,"Symbol":"tvk","Index":279},{"TotalEquity":0,"TotalDebt":0,"BasePrice":14100000000,"Symbol":"twt","Index":280},{"TotalEquity":13980000,"TotalDebt":0,"BasePrice":15400000000,"Symbol":"uma","Index":281},{"TotalEquity":19120000,"TotalDebt":0,"BasePrice":39360000000,"Symbol":"unfi","Index":282},{"TotalEquity":11981756100,"TotalDebt":0,"BasePrice":55220000000,"Symbol":"uni","Index":283},{"TotalEquity":0,"TotalDebt":0,"BasePrice":10000650400,"Symbol":"usdc","Index":284},{"TotalEquity":12876907115652,"TotalDebt":0,"BasePrice":9997000900,"Symbol":"usdt","Index":285},{"TotalEquity":220063518946,"TotalDebt":0,"BasePrice":203321700,"Symbol":"ustc","Index":286},{"TotalEquity":0,"TotalDebt":0,"BasePrice":777000000,"Symbol":"utk","Index":287},{"TotalEquity":7430929587566,"TotalDebt":0,"BasePrice":164100000,"Symbol":"vet","Index":288},{"TotalEquity":169058297966,"TotalDebt":0,"BasePrice":694900000,"Symbol":"vib","Index":289},{"TotalEquity":252046634,"TotalDebt":0,"BasePrice":195000000,"Symbol":"vite","Index":290},{"TotalEquity":25254109536,"TotalDebt":0,"BasePrice":1671000000,"Symbol":"voxel","Index":291},{"TotalEquity":5153547313742,"TotalDebt":0,"BasePrice":9237200,"Symbol":"vtho","Index":292},{"TotalEquity":17493828000,"TotalDebt":0,"BasePrice":1658321600,"Symbol":"wan","Index":293},{"TotalEquity":2852616,"TotalDebt":0,"BasePrice":14130000000,"Symbol":"waves","Index":294},{"TotalEquity":20000180,"TotalDebt":0,"BasePrice":440000000,"Symbol":"waxp","Index":295},{"TotalEquity":24776160000000,"TotalDebt":0,"BasePrice":738000,"Symbol":"win","Index":296},{"TotalEquity":2370200,"TotalDebt":0,"BasePrice":52100000000,"Symbol":"wing","Index":297},{"TotalEquity":0,"TotalDebt":0,"BasePrice":80975707300,"Symbol":"wnxm","Index":298},{"TotalEquity":75262779600,"TotalDebt":0,"BasePrice":1347000000,"Symbol":"woo","Index":299},{"TotalEquity":415631596070,"TotalDebt":0,"BasePrice":1401000000,"Symbol":"wrx","Index":300},{"TotalEquity":183890000,"TotalDebt":0,"BasePrice":1916523600,"Symbol":"wtc","Index":301},{"TotalEquity":172906064000000,"TotalDebt":0,"BasePrice":246700,"Symbol":"xec","Index":302},{"TotalEquity":129072400,"TotalDebt":0,"BasePrice":291912400,"Symbol":"xem","Index":303},{"TotalEquity":152986398800,"TotalDebt":0,"BasePrice":751000000,"Symbol":"xlm","Index":304},{"TotalEquity":109317164,"TotalDebt":0,"BasePrice":1548000000000,"Symbol":"xmr","Index":305},{"TotalEquity":1954309930640,"TotalDebt":0,"BasePrice":3442000000,"Symbol":"xrp","Index":306},{"TotalEquity":388360923948,"TotalDebt":0,"BasePrice":7720000000,"Symbol":"xtz","Index":307},{"TotalEquity":45916405132400,"TotalDebt":0,"BasePrice":27200000,"Symbol":"xvg","Index":308},{"TotalEquity":1725600,"TotalDebt":0,"BasePrice":42900000000,"Symbol":"xvs","Index":309},{"TotalEquity":1940,"TotalDebt":0,"BasePrice":54420000000000,"Symbol":"yfi","Index":310},{"TotalEquity":393918000,"TotalDebt":0,"BasePrice":1749000000,"Symbol":"ygg","Index":311},{"TotalEquity":4124782260,"TotalDebt":0,"BasePrice":414000000000,"Symbol":"zec","Index":312},{"TotalEquity":1900092,"TotalDebt":0,"BasePrice":84900000000,"Symbol":"zen","Index":313},{"TotalEquity":2075635646560,"TotalDebt":0,"BasePrice":174100000,"Symbol":"zil","Index":314},{"TotalEquity":119194400,"TotalDebt":0,"BasePrice":1603000000,"Symbol":"zrx","Index":315}]
}
```

`ProofCsv` : Specify the path of the proof.csv table

`ZkKeyVKDirectoryAndPrefix`: Specify the path and prefix of the zkpor verify key

`CexAssetsInfo`: Exchange assets, obtained from the above command query

### Files required to verify user assets

- Provide `user_config.json` file

We need to use the `userproof` table generated in the above user proof stage, then find the user according to the unique identifier of the exchange user assets in `example_users.csv` previously provided, corresponding to the `account_id` field in the `userproof` table. We query the `config` field, save it in `user_config.json`, and provide it for user download.

The structure of the user_config.json file is as follows

```Plaintext
{
  "Arrangement":7,
  "UniqueIdentification":"00010b7c0a8b51bfa5eca14f0068670bd7fda4063f9bcac4f02c44a00144a80c",
  "TotalAssetEquity":445548224227483774000,
  "TotalAssetDebt":0,
  "AssetDetails":[{"Index":48,"Equity":280,"Debt":0},{"Index":53,"Equity":1020,"Debt":0},{"Index":54,"Equity":3261550200000000,"Debt":0},{"Index":72,"Equity":108600,"Debt":0},{"Index":91,"Equity":9068922000,"Debt":0},{"Index":190,"Equity":13752000,"Debt":0},{"Index":285,"Equity":70860,"Debt":0}],
  "TreeRootHash":"2da42ab6586ef6ad51b4bc8063ce92dcefb951572a26597346b7f78c1329ef0b",
  "MerkleProofEncode":["EmvQ5Sh50gHD96PfN2/o49gT7xVuuX3P22KLVmpWyVo=","JLEw2CGGAPi2TWn7GMbdlwT0wJbpVfJ4A+XLXNYz9X4=","BRCCQWeZy3fmPgiciBNdDMmugJtcQnxfI/b0EU4MlR8=","K8P8ZvYSY9iEreGnatTO8h1/I3Q+ZSkBA3TYYI1vN1g=","GwxhwdTBri22QcY4Pj9B3TkkLpOTGlCpqnsmxVquaeQ=","JIB+i/tDXSbEyK5ASwx2Tgbtm2ckJrJ30qnLm3FGhvs=","I0AzcupyH3clJooxcjaZlOIWOTY531UBJIMpfu2ds9o=","GYU5H/xfC18jR4LXz3axjKgJOaAbSAz3vO/taxTTMDE=","GML/iwCEjgYlSAmd4cQQhKsjH+xscIG6hbM5HP+OP/I=","BBXHrrH1oIGsjK1PsZt1d+ovsDW5IvHxFUlt8CJ3j/M=","F6GyEMWOjvKBgKDCCkQiOfc5SvGEt2MWyQTzszXzd6Y=","JDZjD4o0q6cGYJzj0BBaBEBEN4y4UjYgMSNIXf2P6Ps=","C+Mh1228yGv2Or6yQs3U0sjBzxxWJPTyH5GNG3FzMbk=","Jpo3tkE2KgMxWoEdMM1sOyJsM9YjsI9aONsEEqmMPnA=","FaWOvl42fYbklbc9WgWFqeW3Q/54KXT5zYdIGyCh9iE=","EvcLzRuRio6YT9QjSPp0GGGFYSIW8fKOqQlcOXFBBwo=","LJos88T9kz5kG0o+yeNX0ij+WwrOEIqRVpJtOrUrnns=","CFv3HhUsTXNa3iT/cc+GhD9lV+weuSWoJJRVgZmn7fQ=","EyfPjcon6R+nXBDT/9++ddQqlxiBaSaTMBiC0R6NPoM=","HOtPMAkz3JJG3n0bxNIqkR1p/Q758Em1Jjn1KE6A2mg=","Lq3n7B3Bs7ILnDLG17szIf9O0OdotsWpSLwejnJVcLY=","HthvmzZ/MHbOWVSuFyc9sUvuSz0ddveEwoyQExrim5k=","BOxHEGxRtmNch1R57kgKMxiBVnR/tCo9y3XcJco7Saw=","Dilkpy2L945iR+BsbaffA7MBZSNofd2PdZSkzN48DOE=","Fotw+U5orv9231KkpBYOXM+odtZGgCaNw5zOY+xZ5Oc=","J7pOZTvxtC7B8RzevUvrd90GfrH2oxtRqkEF+mFdCuc=","EUZQwQDUH48osqrtgcPuAQsQvdVKTC+hYmKvIhzImZQ=","HKC2vx3pnDTdfyrzYjCbJMcxojJfvuyzj2/rMMiMplQ="]
}
```

## Final User Content

So the file structure the user finally gets is roughly as follows:

```Plaintext
- config
    cex_config.json
    user_config.json
    proof.csv
zkpor864.vk.save
main
```

> Binary file `main` may have different names depending on the device

- Mac OS (Intel): zkproof_darwin_amd64
- Mac OS (M1): zkproof_darwin_arm64
- Linux: zkproof_linux_amd64
- Windows: zkproof_windows_amd64.exe

## User Verifies Exchange Assets

Run the following command to start the verification

```Plaintext
./main verify cex
```

If the verification is successful, it will output

```Plaintext
All proofs verify passed!!!
```

## User Verifies Their Own Assets

```Plaintext
./main verify user
```

If the verification is successful, it will output

```Plaintext
merkle leave hash: 164bc38a71b7a757455d93017242b4960cd1fea6842d8387b60c5780205858ce
verify pass!!!
```

## Contribution

We welcome all friends who are interested in decentralized exchanges, zk-SNARK, and MerkleTree technology to participate in this project. Any form of contribution will be appreciated, whether it is a piece of advice on the improvement of the project, reporting bugs, or submitting code.


## License
Copyright 2023 © Gate Technology Inc.. All rights reserved.

Licensed under the GPLv3 license.
